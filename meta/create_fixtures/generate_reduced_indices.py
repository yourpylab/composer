import json
import csv
from collections import deque
from typing import List, Dict, Set, Deque
import os

basepath: str = os.path.join("/dmz", "github", "analysis", "composer")
index_path: str = os.path.join(basepath, "tmp", "efile_indices")

retained_fp: str = os.path.join(index_path, "retained_efiles.csv")
with open(retained_fp) as fh:
    reader: csv.DictReader = csv.DictReader(fh)
    object_ids: Set = {row["ObjectId"] for row in reader}

for year in range(2011, 2020):
    file_name: str = "index_%i.json" % year
    original_path: str = os.path.join(index_path, file_name)
    reduced_path: str = os.path.join(basepath, "fixtures", "efile_indices", "second_timepoint", file_name)
    print(file_name)
    with open(original_path) as o_fh, open(reduced_path, "w") as r_fh:
        raw: Dict = json.load(o_fh)
        assert len(raw) == 1
        key: str = next(iter(raw.keys()))
        efiles: List[Dict] = raw[key]
        ret: Deque = deque()
        for efile in efiles:
            if efile["ObjectId"] in object_ids:
                ret.append(efile)
        reduced: Dict = {key: list(ret)}
        json.dump(reduced, r_fh, indent=2)
