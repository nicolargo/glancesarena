from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Tuple


@dataclass
class Stat:
    value: float | None = None
    retention: int = 0
    history: List[Tuple[datetime, float]] = field(default_factory=list)

    def __post_init__(self):
        self._previous_timestamp: datetime | None = None
        self._previous_value: float | None = None

    def reset(self):
        self.value = None
        self._previous_timestamp = None
        self._previous_value = None
        self.history = []

    def update(self, value: float, rate: bool = False, precision: int | None = None):
        if rate:
            now = datetime.now()
            if self._previous_value is not None:
                self.value = round((value - self._previous_value) / (now - self._previous_timestamp).total_seconds(),
                                   precision)
            self._previous_timestamp = now
            self._previous_value = value
        else:
            self.value = value

        if self.retention > 0 and self.value is not None:
            if len(self.history) >= self.retention:
                self.history.pop(0)
            self.history.append((datetime.now(), self.value))

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
