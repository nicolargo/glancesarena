from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Tuple


@dataclass
class History:
    retention: int | None = None
    history: List[Tuple[datetime, float]] = field(default_factory=list)

    def reset(self):
        self.history = []

    def append(self, value: float):
        if self.retention is not None and len(self.history) >= self.retention:
            self.history.pop(0)
        self.history.append((datetime.now(), value))

    def mean(self) -> float | None:
        if len(self.history) == 0:
            return None
        return sum([x[1] for x in self.history]) / len(self.history)

    def max(self) -> float | None:
        if len(self.history) == 0:
            return None
        return max([x[1] for x in self.history])

    def min(self) -> float | None:
        if len(self.history) == 0:
            return None
        return min([x[1] for x in self.history])
