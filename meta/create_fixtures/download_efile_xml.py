import os
from sqlite3 import Connection, connect
import requests
from composer.efile.index import EfileIndex

basepath: str = "/dmz/github/analysis/composer/fixtures"

for timepoint in ["first", "second"]:
    db_path: str = "%s/sqlite/%s_timepoint.sqlite" % (basepath, timepoint)
    conn: Connection = connect(db_path)
    index: EfileIndex = EfileIndex.build(conn)
    for filing in index.latest_filings:
        url: str = filing.url
        filename: str = url.split("/")[-1]
        dest_path: str = "%s/efile_xml/%s" % (basepath, filename)
        if os.path.exists(dest_path):
            continue
        print("Downloading %s" % filename)
        response: requests.Response = requests.get(url)
        open(dest_path, "wb").write(response.content)
