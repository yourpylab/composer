import os
from collections import Callable
from typing import Optional

from mock import MagicMock

import pytest

from composer.aws.s3 import Bucket

BASEPATH: str = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture()
def file_backed_bucket() -> Callable:
    def _ret(root_dir: str) -> Bucket:
        bucket: Bucket = MagicMock(spec=Bucket)

        def get_file_content(filename: str, encoding: Optional[str]="utf-8") -> str:
            filepath: str = os.path.join(root_dir, filename)
            with open(filepath) as fh:
                return fh.read()

        bucket.get_obj_body.side_effect = get_file_content

        def file_exists(filename: str) -> bool:
            filepath: str = os.path.join(root_dir, filename)
            return os.path.exists(filepath)

        bucket.exists.side_effect = file_exists
        return bucket

    return _ret

@pytest.fixture()
def fixture_path() -> str:
    return os.path.join(BASEPATH, "..", "fixtures")
