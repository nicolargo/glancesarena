from dataclasses import dataclass

from glances_stat import Stat


@dataclass
class Plugin:
    name: str
    key: str | None = None
    stats: dict[str, Stat] = None

    # TODO: make a class to init all the stats with name, unit... like is done for field_definition
    def __post_init__(self):
        pass

    def reset(self):
        if self.stats is not None:
            for stat in self.stats.values():
                stat.reset()

    def update(self, key: str, value: float):
        if self.stats is None:
            self.stats = {}
        if key not in self.stats:
            self.stats[key] = Stat('')
        self.stats[key].update(value)
