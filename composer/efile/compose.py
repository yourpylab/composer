import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Iterator, Tuple, Dict, List, Iterable
import json

from concurrent.futures import Future, as_completed, ThreadPoolExecutor

from composer.aws.efile.filings import RetrieveEfiles
from composer.aws.s3 import Bucket
from composer.efile.structures.metadata import FilingMetadata
from composer.fileio.paths import EINPathManager
from composer.conf import MAX_WORKERS, JSON_FILENAME, UPDATE_TIMEOUT


@dataclass
class ComposeEfiles(Callable):
    retrieve: RetrieveEfiles
    path_mgr: EINPathManager

    @classmethod
    def build(cls, basepath: str, bucket: Bucket, temp_path: str, no_cleanup: bool) -> "ComposeEfiles":
        retrieve: RetrieveEfiles = RetrieveEfiles(bucket, temp_path, no_cleanup)
        path_mgr: EINPathManager = EINPathManager(basepath)
        return cls(retrieve, path_mgr)

    def process_all(self, json_changes: Iterable[Tuple[str, Dict[str, str]]]):
        updater = ComposeEfilesUpdater(self.path_mgr)
        
        # NOTE: consider using max_workers setting, set it in conf file. 
        # I don't consider the following block as a cpu-bound, 
        # it contains file i/o operations; even if you process a huge file, 
        # and file translation take a lot of time, file i/o take much
        # biggere time. Consider using ThreadPoolExecutor instead.
        exceptions = []
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(updater.create_or_update, change) for change in json_changes]
            for future in as_completed(futures, timeout=UPDATE_TIMEOUT):
                if future.exception() is not None:
                    exceptions.append(future.exception())

        if len(exceptions) > 0:
            raise exceptions[0]

    def __call__(self, changes: Iterator[Tuple[str, Dict[str, FilingMetadata]]]):
        """Iterate over EINs flagged as having one or more new e-files since the last update. For each one, create or
        update its composite with the new data.

        :param changes: Iterator of (EIN, dictionary of (filing period -> Filing)).
        """

        change_list: List = list(changes)
        json_changes: Iterable[Tuple[str, Dict[str, str]]] = list(self.retrieve(change_list))
        logging.info("Updating e-file composites.")

        self.process_all(json_changes)


@dataclass
class ComposeEfilesUpdater:
    path_mgr: EINPathManager

    def _get_existing(self, ein: str) -> Dict:
        try:
            with self.path_mgr.open_for_reading(ein, JSON_FILENAME) as fh:
                return json.load(fh)
        except FileNotFoundError:
            return {}

    def create_or_update(self, change: Tuple[str, Dict[str, str]]):
        ein, updates = change
        composite: Dict = self._get_existing(ein)
        for period, json_path in updates.items():
            with open(json_path) as fh:
                content: Dict = json.load(fh)
            composite[period] = content
        with self.path_mgr.open_for_writing(ein, JSON_FILENAME) as fh:
            json.dump(composite, fh, indent=2)
