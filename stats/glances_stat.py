from dataclasses import dataclass, field


@dataclass
class Stat:
    unit: str
    value: float | None = None
    retention: int | None = None
    history: list[float] = field(default_factory=list)

    def reset(self):
        self.value = None
        self.history = []

    def update(self, value: float):
        self.value = value
        if self.retention is not None and len(self.history) >= self.retention:
            self.history.pop(0)
        self.history.append(value)

    def mean(self) -> float | None:
        if len(self.history) == 0:
            return None
        return sum(self.history) / len(self.history)

    def max(self) -> float | None:
        if len(self.history) == 0:
            return None
        return max(self.history)

    def min(self) -> float | None:
        if len(self.history) == 0:
            return None
        return min(self.history)
