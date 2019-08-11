import logging
import time
from dataclasses import dataclass, field
from typing import Optional, Callable

@dataclass
class TimeLogger:
    template: str
    chunk_size: int = field(default=1000)
    elapsed_tot: float = field(default=0.0, init=False)
    elapsed_chunk: float = field(default=0.0, init=False)
    start_time: Optional[float] = field(default=None, init=False)
    count: int = field(default=0, init=False)

    def measure(self, fn: Callable):
        self.start_time = time.time()
        fn()
        self.elapsed_chunk = time.time() - self.start_time
        self.count += 1
        if self.count % self.chunk_size == 0:
            self.log(self.chunk_size)

    def log(self, chunk_count):
        self.elapsed_tot += self.elapsed_chunk
        count_message: str = self.template.format(self.count)
        chunk_avg: float = self.elapsed_chunk / chunk_count * 1e9
        overall_avg: float = self.elapsed_tot / self.count * 1e9
        timing_message: str = "(chunk avg: %0.02fns | overall avg %0.02fns)" % (chunk_avg, overall_avg)
        full_message: str = "%s %s" % (count_message, timing_message)
        logging.info(full_message)

    def finish(self):
        chunk_count: int = self.count % self.chunk_size
        self.log(chunk_count)