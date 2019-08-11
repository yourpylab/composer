import os
from collections import Callable
from typing import Optional

from mock import MagicMock

import pytest

from composer.aws.s3 import Bucket

BASEPATH: str = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture()
def fixture_path() -> str:
    return os.path.join(BASEPATH, "..", "fixtures")
