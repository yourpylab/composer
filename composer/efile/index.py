from collections import defaultdict
from dataclasses import field
from typing import Iterator, Dict, Tuple, List, TYPE_CHECKING, NamedTuple
import sqlite3
from attr import dataclass

@dataclass
class EfileIndex:
    """SQLite-backed index of:
        (1) latest e-files for each EIN/period combination.
        (2) known duplicates of any EIN/period combinations.

        Stages change information and commits on demand.
    """

    db: sqlite3.Connection
    _new: Dict[str, Dict[str, Dict[str, str]]] = field(default_factory=lambda: defaultdict(dict), init=False)
    _amended: Dict[str, Dict[str, Dict[str, str]]] = field(default_factory=lambda: defaultdict(dict), init=False)

    @property
    def eins(self) -> Iterator[str]:
        """Yields all distinct EINs that have e-filed as of the most recent commit."""
        pass

    @property
    def changes(self) -> Iterator[Tuple[str, Dict[str, str]]]:
        """Yields all EINs that have at least one change since the last commit, along with a dictionary of period ->
        IRS object ID for those changes."""
        pass

    def filings(self, ein: str) -> Iterator[Dict]:
        """Yields dictionaries representing the e-file metadata for all filing periods associated with an EIN as of the
        last commit. If more than one filing has been filed for the same period, only returns the latest one."""
        pass

    def add(self, filing: Dict) -> None:
        """Stages a filing for recording. If a filing for the same EIN/period combination exists, either stages it for
        adding to duplicates or to changes depending on date relative to existing. Does not commit."""
        pass

    def duplicates(self) -> Iterator[Dict]:
        """Yields dictionaries representing e-file metadata for all filings that have been superceded by other filings;
        i.e., for which a newer filing exists for the same EIN/period combination."""
        pass

    def commit(self):
        """Commits all changes that were staged."""
        pass