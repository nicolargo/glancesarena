from dataclasses import dataclass

from glances_stat import Stat


@dataclass
class Plugin:
    name: str
    key: str | None = None
    stats: dict[str, Stat] = None

    def update(self, key: str, value: float):
        if self.stats is None:
            self.stats = {}
        if key not in self.stats:
            self.stats[key] = Stat('')
        self.stats[key].update(value)
