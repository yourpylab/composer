"""The IRS provides two sets of index files for the 990 e-file dataset: one in CSV and one in JSON. Unfortunately, the
CSV dataset has less information. So this script creates a master CSV file that I can then mine for test fixtures."""

import os
import csv
import json
from typing import List, Dict

basepath: str = os.path.join("/dmz", "github", "analysis", "composer")
index_path: str = os.path.join(basepath, "tmp", "efile_indices")

columns: List[str] = [
    "RecordID",
    "EIN",
    "TaxPeriod",
    "DLN",
    "FormType",
    "URL",
    "OrganizationName",
    "SubmittedOn",
    "ObjectId",
    "LastUpdated",
    "IndexFile"
]
with open("%s/all_efiles.csv" % index_path, "w") as csv_fh:
    writer: csv.DictWriter = csv.DictWriter(csv_fh, columns)
    writer.writeheader()
    for year in range(2011, 2020):
        file_name: str = "index_%i.json" % year
        file_path: str = os.path.join(index_path, file_name)
        print(file_path)
        with open(file_path) as json_fh:
            raw: Dict = json.load(json_fh)
            assert len(raw) == 1
            key: str = next(iter(raw.keys()))
            efiles: List[Dict] = raw[key]
            for efile in efiles:
                efile["IndexFile"] = file_name
                record_id: str = "%s_%s" % (efile["EIN"], efile["TaxPeriod"])
                efile["RecordID"] = record_id
                writer.writerow(efile)
