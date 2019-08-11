from collections.abc import Callable
from dataclasses import dataclass
from typing import Iterator, Tuple, Dict
import json

from composer.aws.efile.filings import EfileFilings
from composer.efile.structures.metadata import FilingMetadata
from composer.fileio.paths import EINPathManager

TEMPLATE = "%s.json"

@dataclass
class ComposeEfiles(Callable):
    s3_filings: EfileFilings
    path_mgr: EINPathManager

    def _get_existing(self, ein: str) -> Dict:
        try:
            with self.path_mgr.open_for_reading(ein, TEMPLATE) as fh:
                return json.load(fh)
        except FileNotFoundError:
            return {}

    def _create_or_update(self, ein: str, updates: Dict[str, FilingMetadata]):
        composite: Dict = self._get_existing(ein)
        for period, metadata in updates.items():
            content = self.s3_filings[metadata.irs_efile_id]
            composite[period] = content
        with self.path_mgr.open_for_writing(ein, TEMPLATE) as fh:
            json.dump(composite, fh, indent=2)

    def __call__(self, changes: Iterator[Tuple[str, Dict[str, FilingMetadata]]]):
        """Iterate over EINs flagged as having one or more new e-files since the last update. For each one, create or
        update its composite with the new data.

        :param changes: Iterator of (EIN, dictionary of (filing period -> Filing)).
        """

        # TODO Make concurrent
        changes = list(changes)
        for ein, updates in changes:
            self._create_or_update(ein, updates)