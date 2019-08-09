import json
import os
from sqlite3 import Connection, connect
from typing import Dict, List

from composer.efile.filing import Filing
from composer.efile.index import EfileIndex
from composer.efile.sqlite import init_sqlite_db

basepath: str = "/dmz/github/analysis/composer/fixtures"
date_loaded: str = "2019-08-07 06:05:04"
for timepoint in ["first", "second"]:
    db_path: str = "%s/sqlite/%s_timepoint.sqlite" % (basepath, timepoint)
    conn: Connection = init_sqlite_db(db_path)
    index: EfileIndex = EfileIndex.build(conn)
    for year in range(2011, 2020):
        json_path: str = "%s/efile_indices/%s_timepoint/index_%i.json" % (basepath, timepoint, year)
        if not os.path.exists(json_path):
            print("Skipping %s" % json_path)
            continue
        with open(json_path) as fh:
            raw: Dict = json.load(fh)
            filings: List = raw[list(raw.keys())[0]]
            for filing_spec in filings:
                filing: Filing = Filing.from_json(filing_spec)
                filing.date_downloaded = date_loaded
                index.add(filing)
    print("Committing %s" % db_path)
    index.commit()
    conn.close()
