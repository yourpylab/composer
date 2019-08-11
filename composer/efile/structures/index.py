import sqlite3
from collections import defaultdict, deque
from dataclasses import field, dataclass
from typing import Iterator, Dict, Tuple, List, Deque

from composer.efile.structures.metadata import FilingMetadata
from composer.efile.structures.sqlite import EfileIndexTable

@dataclass
class EfileIndex:
    """SQLite-backed index of:
        (1) latest e-files for each EIN/period combination.
        (2) known duplicates of any EIN/period combinations.

        Stages change information and commits on demand.
    """

    duplicates: EfileIndexTable
    latest_filings: EfileIndexTable
    staged_changes: Dict[str, Dict[str, FilingMetadata]] = field(default_factory=lambda: defaultdict(dict), init=False)
    staged_dupes: Deque[FilingMetadata] = field(default_factory=deque, init=False)

    @classmethod
    def build(cls, conn: sqlite3.Connection) -> "EfileIndex":
        duplicates: EfileIndexTable = EfileIndexTable(conn, "duplicates")
        latest_filings: EfileIndexTable = EfileIndexTable(conn, "latest_filings")
        return cls(duplicates, latest_filings)

    @property
    def eins(self) -> Iterator[str]:
        """Yields all distinct EINs that have e-filed as of the most recent commit."""
        yield from self.latest_filings.eins

    @property
    def changes(self) -> Iterator[Tuple[str, Dict[str, FilingMetadata]]]:
        """Yields all EINs that have at least one change since the last commit, along with a dictionary of period ->
        Filing for those changes."""
        yield from self.staged_changes.items()

    def filings(self, ein: str) -> Iterator[FilingMetadata]:
        """Yields dictionaries representing the e-file metadata for all filing periods associated with an EIN as of the
        last commit. If more than one filing has been filed for the same period, only returns the latest one."""
        yield from self.duplicates.filings_for_ein(ein)

    def _choose_new_filing_to_keep(self, filing: FilingMetadata):
        other: FilingMetadata = self.staged_changes[filing.ein][filing.period]
        self._choose_filing_to_keep(filing, other)

    def _choose_between_new_and_existing(self, filing: FilingMetadata):
        existing: List[FilingMetadata] = list(self.latest_filings.filings_by_record_id(filing.record_id))
        assert len(existing) <= 1
        if len(existing) == 1:
            other: FilingMetadata = existing[0]
            self._choose_filing_to_keep(filing, other)
        else:
            self.staged_changes[filing.ein][filing.period] = filing

    def _choose_filing_to_keep(self, filing: FilingMetadata, other: FilingMetadata):
        if other.date_submitted > filing.date_submitted:
            self.staged_dupes.append(filing)
        elif other.date_submitted == filing.date_submitted and other.date_uploaded > filing.date_uploaded:
            self.staged_dupes.append(filing)
        else:
            self.staged_dupes.append(other)
            self.staged_changes[filing.ein][filing.period] = filing

    def add(self, filing: FilingMetadata) -> None:
        """Stages a filing for recording. If a filing for the same EIN/period combination exists, either stages it for
        adding to duplicates or to changes depending on date relative to existing. Does not commit."""
        if filing.ein in self.staged_changes and filing.period in self.staged_changes[filing.ein]:
            self._choose_new_filing_to_keep(filing)
        else:
            self._choose_between_new_and_existing(filing)

    def commit(self):
        """Commits all changes that were staged."""
        for filing in self.staged_dupes:
            self.latest_filings.delete_if_exists(filing.irs_efile_id)
            self.duplicates.upsert(filing)
        self.staged_dupes.clear()

        for change_list in self.staged_changes.values():
            for filing in change_list.values():
                self.latest_filings.upsert(filing)
        self.staged_changes.clear()
