from typing import List, Dict

import pytest
import sqlite3

from composer.efile.index import EfileIndex

@pytest.fixture()
def index(empty_db: sqlite3.Connection) -> EfileIndex:
    return EfileIndex(empty_db)

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
    expected: List = [("943041314", {"201012": "201120919349300412"})]
    actual: List = list(index.changes)
    assert actual == expected

def test_add_original_and_amended_before_commit_stages_both(index):
    pytest.fail()

def test_add_amended_filing_available_as_change_before_commit(index):
    pytest.fail()

def test_add_new_filing_removed_from_changes_after_commit(index):
    pytest.fail()

def test_add_amended_filing_removed_from_changes_after_commit(index):
    pytest.fail()

def test_add_new_filing_not_available_as_ein_before_commit(index):
    pytest.fail()

def test_add_new_filing_not_available_as_filing_before_commit(index):
    pytest.fail()

def test_add_amended_filing_not_available_as_duplicate_before_commit(index):
    pytest.fail()

def test_add_new_filing_available_as_ein_after_commit(index):
    pytest.fail()

def test_add_new_filing_available_as_filing_after_commit(index):
    pytest.fail()

def test_add_amended_filing_vailable_as_duplicate_after_commit(index):
    pytest.fail()

def test_add_new_filing_reflected_in_db_after_commit(index):
    pytest.fail()

def test_add_amended_filing_reflected_in_db_after_commit(index):
    pytest.fail()
