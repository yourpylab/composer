import dataclasses
from collections.abc import Iterable
from sqlite3 import Connection, Cursor, connect
from typing import Dict, Iterator, Optional, Tuple

from attr import dataclass

from composer.efile.structures.metadata import FilingMetadata

@dataclass
class EfileIndexTable(Iterable):
    conn: Connection
    table_name: str

    def __iter__(self) -> Iterator[FilingMetadata]:
        query: str = "SELECT * FROM %s" % self.table_name
        cursor: Cursor = self.conn.cursor()
        for row in cursor.execute(query):
            yield FilingMetadata(*row)

    def upsert(self, filing: FilingMetadata):
        """Inserts or replaces existing row in the table."""
        query: str = "INSERT OR REPLACE INTO %s VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" % self.table_name
        values: Tuple = dataclasses.astuple(filing)
        cursor: Cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()

    def delete_if_exists(self, irs_efile_id: str):
        """Deletes the record from the table, if it exists."""
        query: str = "DELETE FROM %s WHERE irs_efile_id = ?" % self.table_name
        cursor: Cursor = self.conn.cursor()
        cursor.execute(query, (irs_efile_id,))
        self.conn.commit()

    def _filings_by_key(self, key_name: str, key_value: str) -> Iterator[FilingMetadata]:
        query: str = "SELECT * FROM %s WHERE %s = ?" % (self.table_name, key_name)
        cursor: Cursor = self.conn.cursor()
        for row in cursor.execute(query, (key_value,)):
            yield FilingMetadata(*row)

    @property
    def eins(self) -> Iterator[str]:
        query: str = "SELECT DISTINCT ein FROM %s" % self.table_name
        cursor: Cursor = self.conn.cursor()
        for row in cursor.execute(query):
            yield row[0]

    def filings_for_ein(self, ein: str) -> Iterator[FilingMetadata]:
        yield from self._filings_by_key("ein", ein)

    def filings_by_record_id(self, record_id: str) -> Iterator[FilingMetadata]:
        yield from self._filings_by_key("record_id", record_id)

    def filings_by_irs_efile_id(self, irs_efile_id: str) -> Iterator[FilingMetadata]:
        yield from self._filings_by_key("irs_efile_id", irs_efile_id)

def init_sqlite_db(connection_str: str) -> Connection:
    conn: Connection = connect(connection_str)

    cursor: Cursor = conn.cursor()

    # Create the table for latest filings
    cursor.execute("""
        CREATE TABLE latest_filings (
            record_id text PRIMARY KEY,
            irs_efile_id text NOT NULL,
            irs_dln text NOT NULL,
            ein text NOT NULL,
            period text NOT NULL,
            name_org text NOT NULL,
            form_type text NOT NULL,
            date_submitted text NOT NULL,
            date_uploaded text NOT NULL,
            date_downloaded text NOT NULL,
            url text NOT NULL
        );
    """)

    cursor.execute("CREATE INDEX idx_latest_filings_ein ON latest_filings(ein);")
    cursor.execute("CREATE INDEX idx_latest_filings_irs_efile_id ON latest_filings(irs_efile_id);")

    # Create table for duplicates
    cursor.execute("""
        CREATE TABLE duplicates (
            record_id text NOT NULL,
            irs_efile_id text PRIMARY KEY,
            irs_dln text NOT NULL,
            ein text NOT NULL,
            period text NOT NULL,
            name_org text NOT NULL,
            form_type text NOT NULL,
            date_submitted text NOT NULL,
            date_uploaded text NOT NULL,
            date_downloaded text NOT NULL,
            url text NOT NULL
        );
    """)

    cursor.execute("CREATE INDEX idx_duplicates_record_id ON duplicates(record_id);")
    cursor.execute("CREATE INDEX idx_duplicates_ein ON duplicates(ein);")
    conn.commit()

    return conn

