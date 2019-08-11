import logging
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Iterator, Tuple, Dict, Deque
import json

from concurrent.futures import ThreadPoolExecutor, Future, as_completed
from composer.aws.efile.filings import EfileFilings
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
    s3_filings: EfileFilings
    path_mgr: EINPathManager
    t_log: TimeLogger = field(default_factory=lambda: TimeLogger("Updated {:,} e-file composites."), init=False)

    @classmethod
    def build(cls, basepath: str, bucket: Bucket) -> "ComposeEfiles":
        s3_filings: EfileFilings = EfileFilings(bucket)
        path_mgr: EINPathManager = EINPathManager(basepath)
        return cls(s3_filings, path_mgr)

    def _get_existing(self, ein: str) -> Dict:
        try:
            with self.path_mgr.open_for_reading(ein, TEMPLATE) as fh:
                return json.load(fh)
        except FileNotFoundError:
            return {}

    def _do_create_or_update(self, ein: str, updates: Dict[str, FilingMetadata]):
        composite: Dict = self._get_existing(ein)
        for period, metadata in updates.items():
            content = self.s3_filings[metadata.irs_efile_id]
            composite[period] = content
        with self.path_mgr.open_for_writing(ein, TEMPLATE) as fh:
            json.dump(composite, fh, indent=2)

    def _create_or_update(self, ein: str, updates: Dict[str, FilingMetadata]):
        fn: Callable = lambda: self._do_create_or_update(ein, updates)
        self.t_log.measure(fn)

    def enqueue(self, changes) -> Iterator[Future]:
        with ThreadPoolExecutor() as executor:
            for ein, updates in changes:
                yield executor.submit(self._create_or_update, ein, updates)

    def __call__(self, changes: Iterator[Tuple[str, Dict[str, FilingMetadata]]]):
        """Iterate over EINs flagged as having one or more new e-files since the last update. For each one, create or
        update its composite with the new data.

        :param changes: Iterator of (EIN, dictionary of (filing period -> Filing)).
        """
        logging.info("Updating e-file composites.")
        futures: Iterator[Future] = self.enqueue(changes)
        _await_all(futures)
        self.t_log.finish()