from collections.abc import Callable
from dataclasses import dataclass

from composer.aws.efile.indices import EfileIndices
from composer.aws.efile.filings import EfileFilings
from composer.efile.structures.index import EfileMetadataIndex
from composer.efile.compose import ComposeEfiles

@dataclass
class UpdateEfileState(Callable):
    basepath: str
    indices: EfileIndices
    filings: EfileFilings

    def __call__(self):
        pass

