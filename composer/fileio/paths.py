import os
from dataclasses import dataclass
from typing import IO

@dataclass
class EINPathManager:
    basepath: str

    def directory_for(self, ein: str):
        first, second, third = ein[0:3], ein[3:6], ein[6:9]
        return os.path.join(self.basepath, first, second, third)

    def open_for_reading(self, ein: str, template: str) -> IO:
        """Locates a file whose filename conforms to a specified template and corresponding to a particular EIN, then
        opens it for reading.

        :param ein: The EIN whose file should be opened
        :param template: A string template for the filename, where "%s" will represent the EIN
        :return: A file object in read-only mode.
        """

        filename: str = template % ein
        directory: str = self.directory_for(ein)
        filepath: str = os.path.join(directory, filename)
        return open(filepath)

    def open_for_writing(self, ein: str, template: str) -> IO:
        """Creates directories as needed for a file whose filename conforms to a specified template and corresponding to
        a particular EIN, then opens it for writing.

        :param ein: The EIN whose file should be opened
        :param template: A string template for the filename, where "%s" will represent the EIN
        :return: A file object in write mode.
        """

        directory: str = self.directory_for(ein)
        os.makedirs(directory, exist_ok=True)

        filename: str = template % ein
        filepath: str = os.path.join(directory, filename)
        return open(filepath, "w")

    def exists(self, ein: str, template: str) -> bool:
        filename: str = template % ein
        directory: str = self.directory_for(ein)
        filepath: str = os.path.join(directory, filename)
        return os.path.exists(filepath)
