import logging
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Iterator, Tuple, Dict, Deque, List, Iterable
import json

from concurrent.futures import ThreadPoolExecutor, Future, as_completed, ProcessPoolExecutor

from composer.aws.efile.filings import RetrieveEfiles
from composer.aws.s3 import Bucket
from composer.efile.structures.metadata import FilingMetadata
from composer.fileio.paths import EINPathManager
from composer.timer import TimeLogger

TEMPLATE = "%s.json"

def _await_all(futures: Iterator[Future]):
    """Since concurrent.futures doesn't have an await function, this function simply halts further work until all
    futures have completed."""
    for future in as_completed(futures):  # type: Future
        future.result()

@dataclass
class ComposeEfiles(Callable):
    retrieve: RetrieveEfiles
    path_mgr: EINPathManager
    t_log: TimeLogger = field(default_factory=lambda: TimeLogger("Updated {:,} e-file composites."), init=False)

    @classmethod
    def build(cls, basepath: str, bucket: Bucket) -> "ComposeEfiles":
        retrieve: RetrieveEfiles = RetrieveEfiles(bucket)
        path_mgr: EINPathManager = EINPathManager(basepath)
        return cls(retrieve, path_mgr)

    def use_for_loop(self, json_changes: Iterable[Tuple[str, Dict[str, str]]]):
        updater = ComposeEfilesUpdater(self.path_mgr)
        for change in json_changes:
            updater.create_or_update(change)

    def use_process_pool(self, json_changes: Iterable[Tuple[str, Dict[str, str]]]):
        updater = ComposeEfilesUpdater(self.path_mgr)
        exceptions = []
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(updater.create_or_update, change) for change in json_changes]
            for future in as_completed(futures):
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

        # If I use this, it works
        # self.use_for_loop(json_changes)

        # If I instead use this, it does not work -- seems to deadlock
        self.use_process_pool(json_changes)


@dataclass
class ComposeEfilesUpdater:
    path_mgr: EINPathManager

    def _get_existing(self, ein: str) -> Dict:
        try:
            with self.path_mgr.open_for_reading(ein, TEMPLATE) as fh:
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
        with self.path_mgr.open_for_writing(ein, TEMPLATE) as fh:
            json.dump(composite, fh, indent=2)
