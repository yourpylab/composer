from typing import List, Dict

import pytest
import sqlite3

from composer.efile.structures.index import EfileIndex

@pytest.fixture()
def index(empty_db: sqlite3.Connection) -> EfileIndex:
    return EfileIndex.build(empty_db)

def test_empty_db_eins_empty(index):
    expected: List = []
    actual = list(index.eins)
    assert actual == expected

def test_empty_db_changes_empty(index):
    expected: List = []
    actual = list(index.changes)
    assert actual == expected

def test_empty_db_filings_empty(index):
    expected: List = []
    actual = list(index.changes)
    assert actual == expected

def test_add_new_filing_available_as_change_before_commit(index, filing_original):
    index.add(filing_original)
    expected: List = [("943041314", {"201012": filing_original})]
    actual: List = list(index.changes)
    assert actual == expected

def test_add_original_then_amended_before_commit_stages_original_as_dupe(index, filing_original, filing_amended):
    index.add(filing_original)
    index.add(filing_amended)
    expected: List = [filing_original]
    actual: List = list(index.staged_dupes)
    assert actual == expected

def test_add_original_then_amended_before_commit_stages_amended_as_change(index, filing_original, filing_amended):
    index.add(filing_original)
    index.add(filing_amended)
    expected: List = [("943041314", {"201012": filing_amended})]
    actual: List = list(index.changes)
    assert actual == expected

def test_add_amended_then_original_before_commit_stages_original_as_dupe(index, filing_original, filing_amended):
    index.add(filing_amended)
    index.add(filing_original)
    expected: List = [filing_original]
    actual: List = list(index.staged_dupes)
    assert actual == expected

def test_add_amended_then_original_before_commit_stages_amended_as_change(index, filing_original, filing_amended):
    index.add(filing_amended)
    index.add(filing_original)
    expected: List = [("943041314", {"201012": filing_amended})]
    actual: List = list(index.changes)
    assert actual == expected

def test_add_new_filing_not_available_as_filing_before_commit(index, filing_original):
    index.add(filing_original)
    assert list(index.latest_filings) == []

def test_add_new_filing_available_as_filing_after_commit(index, filing_original):
    index.add(filing_original)
    index.commit()
    assert list(index.latest_filings) == [filing_original]

def test_add_new_filing_not_committed_as_dupe(index, filing_original):
    index.add(filing_original)
    index.commit()
    assert list(index.duplicates) == []

def test_add_newer_filing_committed_as_latest(index, filing_original, filing_amended):
    index.add(filing_original)
    index.commit()
    index.add(filing_amended)
    index.commit()
    assert list(index.latest_filings) == [filing_amended]

def test_add_newer_filing_old_becomes_dupe(index, filing_original, filing_amended):
    index.add(filing_original)
    index.commit()
    index.add(filing_amended)
    index.commit()
    assert list(index.duplicates) == [filing_original]

def test_add_older_filing_not_committed_as_latest(index, filing_original, filing_amended):
    index.add(filing_amended)
    index.commit()
    index.add(filing_original)
    index.commit()
    assert list(index.latest_filings) == [filing_amended]

def test_add_older_filing_goes_straight_to_dupe(index, filing_original, filing_amended):
    index.add(filing_amended)
    index.commit()
    index.add(filing_original)
    index.commit()
    assert list(index.duplicates) == [filing_original]

def test_commit_clears_staged_changes(index, filing_original):
    index.add(filing_original)
    assert len(index.staged_changes) == 1
    index.commit()
    assert len(index.staged_changes) == 0

def test_commit_clears_staged_dupes(index, filing_original, filing_amended):
    index.add(filing_original)
    index.add(filing_amended)
    assert len(index.staged_dupes) == 1
    index.commit()
    assert len(index.staged_dupes) == 0

