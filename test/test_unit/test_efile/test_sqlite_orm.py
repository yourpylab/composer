import dataclasses
from collections.abc import Callable
from sqlite3 import Connection, Cursor
from typing import List, Set, Tuple

import pytest

from composer.efile.structures.filing import Filing
from composer.efile.structures.sqlite import EfileIndexTable

tables: List = ["latest_filings", "duplicates"]

@pytest.fixture()
def alpha_filing_1() -> Filing:
    return Filing(
        '0123456789_201012',
        'abcdefghijklmnopqrstuvwxyz',
        'abcdefghijk',
        '0123456789',
        '201012',
        'The Alphabet Company',
        '990',
        '2011-04-15',
        '2016-05-01',
        '2019-08-07',
        'https://example.com/foo'
    )

@pytest.fixture()
def alpha_filing_2() -> Filing:
    return Filing(
        '0123456789_201112',
        'zyxwvutsrqponmlkjihgfedcba',
        'zyxwvutsrqp',
        '0123456789',
        '201112',
        'The Alphabet Company',
        '990',
        '2012-04-15',
        '2016-05-02',
        '2019-08-08',
        'https://example.com/bar'
    )

@pytest.fixture()
def preloaded_orm(empty_db: Connection, alpha_filing_1, alpha_filing_2) -> Callable:
    def _preloaded_orm(table) -> EfileIndexTable:
        cursor: Cursor = empty_db.cursor()
        query = "INSERT INTO %s VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);" % table
        cursor.execute(query, dataclasses.astuple(alpha_filing_1))
        cursor.execute(query, dataclasses.astuple(alpha_filing_2))
        #empty_db.commit()
        return EfileIndexTable(empty_db, table)
    return _preloaded_orm

@pytest.mark.parametrize("table", tables)
def test_upsert_new(preloaded_orm, table, filing_original, alpha_filing_1, alpha_filing_2):
    orm: EfileIndexTable = preloaded_orm(table)
    orm.upsert(filing_original)
    #orm.commit()
    cursor: Cursor = orm.conn.cursor()
    cursor.execute("SELECT * FROM %s" % table)
    expected = {
        dataclasses.astuple(alpha_filing_1),
        dataclasses.astuple(alpha_filing_2),
        dataclasses.astuple(filing_original)
    }
    actual = set(cursor.fetchall())
    assert expected == actual

def test_upsert_existing_duplicates(preloaded_orm, filing_original, alpha_filing_2):
    """Since the primary key for duplicates is efile ID, try to upsert with alpha_filing_1's efile ID"""
    orm: EfileIndexTable = preloaded_orm("duplicates")
    filing_original.irs_efile_id = "abcdefghijklmnopqrstuvwxyz"
    orm.upsert(filing_original)
    #orm.commit()
    cursor: Cursor = orm.conn.cursor()
    cursor.execute("SELECT * FROM duplicates")
    expected = {
        dataclasses.astuple(alpha_filing_2),
        dataclasses.astuple(filing_original)
    }
    actual = set(cursor.fetchall())
    assert expected == actual

def test_upsert_existing_latest_filings(preloaded_orm, filing_original, alpha_filing_1):
    """Since the primary key for latest filings is record ID, try to upsert with alpha_filing_2's record ID"""
    orm: EfileIndexTable = preloaded_orm("latest_filings")
    filing_original.record_id = "0123456789_201112"
    orm.upsert(filing_original)
    #orm.commit()
    cursor: Cursor = orm.conn.cursor()
    cursor.execute("SELECT * FROM main.latest_filings")
    expected = {
        dataclasses.astuple(alpha_filing_1),
        dataclasses.astuple(filing_original)
    }
    actual = set(cursor.fetchall())
    assert expected == actual

@pytest.mark.parametrize("table", tables)
def test_delete_existing(preloaded_orm, table, alpha_filing_2):
    orm: EfileIndexTable = preloaded_orm(table)
    orm.delete_if_exists("abcdefghijklmnopqrstuvwxyz")
    #orm.commit()
    cursor: Cursor = orm.conn.cursor()
    cursor.execute("SELECT * FROM %s" % table)
    expected = {
        dataclasses.astuple(alpha_filing_2)
    }
    actual = set(cursor.fetchall())
    assert expected == actual

@pytest.mark.parametrize("table", tables)
def test_try_to_delete_absent_does_nothing(preloaded_orm, table, alpha_filing_1, alpha_filing_2):
    orm: EfileIndexTable = preloaded_orm(table)
    orm.delete_if_exists("foo bar")
    #orm.commit()
    cursor: Cursor = orm.conn.cursor()
    cursor.execute("SELECT * FROM %s" % table)
    expected: Set[Tuple] = {
        dataclasses.astuple(alpha_filing_1),
        dataclasses.astuple(alpha_filing_2)
    }
    actual: Set[Tuple] = set(cursor.fetchall())
    assert expected == actual

@pytest.mark.parametrize("table", tables)
def test_filings_for_ein_none_exist(preloaded_orm, table):
    orm: EfileIndexTable = preloaded_orm(table)
    expected: List[Filing] = []
    actual = list(orm.filings_for_ein("943041314"))
    assert expected == actual

@pytest.mark.parametrize("table", tables)
def test_filings_for_ein_two_present(preloaded_orm, table, alpha_filing_1, alpha_filing_2):
    orm: EfileIndexTable = preloaded_orm(table)
    expected: List[Filing] = [alpha_filing_1, alpha_filing_2]
    actual: List[Filing] = sorted(orm.filings_for_ein("0123456789"), key=lambda x: x.period)
    assert expected == actual

@pytest.mark.parametrize("table", tables)
def test_filings_by_record_id_exists(preloaded_orm, table, alpha_filing_1):
    orm: EfileIndexTable = preloaded_orm(table)
    assert list(orm.filings_by_record_id("0123456789_201012")) == [alpha_filing_1]

@pytest.mark.parametrize("table", tables)
def test_filings_by_record_id_absent(preloaded_orm, table):
    orm: EfileIndexTable = preloaded_orm(table)
    assert list(orm.filings_by_record_id("943041314_201012")) == []

@pytest.mark.parametrize("table", tables)
def test_filings_by_irs_efile_id_exists(preloaded_orm, table, alpha_filing_1):
    orm: EfileIndexTable = preloaded_orm(table)
    assert list(orm.filings_by_irs_efile_id("abcdefghijklmnopqrstuvwxyz")) == [alpha_filing_1]

@pytest.mark.parametrize("table", tables)
def test_filings_by_irs_efile_id_absent(preloaded_orm, table):
    orm: EfileIndexTable = preloaded_orm(table)
    assert list(orm.filings_by_irs_efile_id("201120919349300412")) == []

@pytest.mark.parametrize("table", tables)
def test_eins(preloaded_orm, table):
    orm: EfileIndexTable = preloaded_orm(table)
    assert list(orm.eins) == ["0123456789"]

@pytest.mark.parametrize("table", tables)
def test_iter(preloaded_orm, table, filing_original, alpha_filing_1, alpha_filing_2):
    orm: EfileIndexTable = preloaded_orm(table)
    orm.upsert(filing_original)
    #orm.commit()
    expected: List = [alpha_filing_1, alpha_filing_2, filing_original]
    actual: List = sorted(orm, key=lambda f: f.record_id)
    assert actual == expected