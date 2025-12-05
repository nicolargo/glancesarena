from dataclasses import dataclass

from glances_stat import Stat


@dataclass
class Plugin:
    definition: dict[str, dict]
    retention: int | None = None
    stats: dict[str, Stat] = None

    def __post_init__(self):
        self.retention = self.retention if self.retention is not None else 100

    def reset(self):
        if self.stats is not None:
            for stat in self.stats.values():
                stat.reset()

    def update(self, field_key: str, field_value: float, key: str | None = None):
        if self.stats is None:
            self.stats = {}

        if self.definition.get('key') and key not in self.stats:
            self.stats[key] = dict()

        if self.definition.get('key'):
            if field_key not in self.stats[key]:
                self.stats[key][field_key] = Stat(retention=self.retention)
            self.stats[key][field_key].update(field_value)
        else:
            if field_key not in self.stats:
                self.stats[field_key] = Stat(retention=self.retention)
            self.stats[field_key].update(field_value)


class CpuPlugin(Plugin):
    definition = {
        'name': 'cpu',
        'key': None,
        'fields': {
            'total': {
                'description': 'CPU Total Usage',
                'unit': '%'
            }
        }
    }

    def __init__(self, retention: int | None = None):
        super().__init__(self.definition, retention=retention)


class NetworkPlugin(Plugin):
    definition = {
        'name': 'network',
        'key': 'interface',
        'fields': {
            'bytes_recv': {
                'description': 'Network Received Bytes',
                'unit': 'byte',
                'rate': True
            }
        }
    }

    def __init__(self, retention: int | None = None):
        super().__init__(self.definition, retention=retention)
