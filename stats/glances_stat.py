from dataclasses import dataclass, field

from glances_history import History


@dataclass
class Stat:
    unit: str | None = None
    value: float | None = None
    retention: int | None = None
    history: History = field(default_factory=History)

    def __post_init__(self):
        self.history = History(self.retention)

    def reset(self):
        self.value = None
        self.history.reset()

    def update(self, value: float):
        self.value = value
        self.history.append(value)

    def mean(self) -> float | None:
        return self.history.mean()

    def max(self) -> float | None:
        return self.history.max()

    def min(self) -> float | None:
        return self.history.min()
