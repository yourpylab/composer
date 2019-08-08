from composer.efile.sqlite import init_sqlite_db
from sqlite3 import Connection

conn: Connection = init_sqlite_db("/dmz/github/analysis/composer/fixtures/sqlite/initial.sqlite")
conn.close()
