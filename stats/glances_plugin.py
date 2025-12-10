from dataclasses import asdict, dataclass

from glances_stat import Stat


@dataclass
class Plugin:
    definition: dict[str, dict]
    stats: dict[str, Stat] = None

    def reset(self):
        if self.stats is not None:
            for stat in self.stats.values():
                stat.reset()

    def _create_stats(self, field_key: str, key: str | None = None, rate: bool = False) -> Stat:
        if self.stats is None:
            self.stats = {}

        # If retention is defined, use it, else no retention (=0)
        retention = self.definition['fields'][field_key].get('retention', 0)

        # Manage rate stats
        if rate:
            field_key = f'{field_key}_rate'

        if self.definition.get('key'):
            # Plugin as a key (example: network)
            if key not in self.stats:
                self.stats[key] = dict()
            if field_key not in self.stats[key]:
                self.stats[key][field_key] = Stat(retention=retention)
            stats = self.stats[key][field_key]
        else:
            # Plugin as no key (example: cpu)
            if field_key not in self.stats:
                self.stats[field_key] = Stat(retention=retention)
            stats = self.stats[field_key]
        return stats

    def update_field(self, field_key: str, field_value: float, key: str | None = None):
        stats = self._create_stats(field_key, key)
        # Manage rate
        if 'rate' in self.definition['fields'][field_key] and self.definition['fields'][field_key]['rate']:
            rate_stats = self._create_stats(field_key, key, rate=True)
            rate_stats.update(field_value, rate=True)
        stats.update(field_value)

    def get_definition(self, key: str | None = None) -> dict:
        if key is None:
            return self.definition
        else:
            return self.definition['fields'].get(key, {})

    @property
    def name(self) -> str:
        return self.definition['name']

    @property
    def description(self) -> str:
        return self.definition['description']

    def get_stats(self, key: str | None = None) -> dict:
        if key is None:
            return {k: asdict(v) for k, v in self.stats.items()}
        elif key in self.stats:
            return asdict(self.stats[key])
        else:
            return {}

    def get_history(self, key: str | None = None) -> dict:
        if key is None:
            return {k: v.history for k, v in self.stats.items()}
        elif key in self.stats:
            return self.stats[key].history
        else:
            return {}


class CpuPlugin(Plugin):
    definition = {
        'name': 'cpu',
        'description': 'CPU plugin',
        'fields': {
            'total': {
                'description': 'Total CPU Usage',
                'unit': '%',
                'retention': 3
            },
            'system': {
                'description': 'System CPU Usage',
                'unit': '%',
                # 'retention': 0
            }
        }
    }

    def __init__(self):
        super().__init__(self.definition)


class NetworkPlugin(Plugin):
    definition = {
        'name': 'network',
        'description': 'Network plugin',
        'key': 'interface',
        'fields': {
            'bytes_recv': {
                'description': 'Network Received Bytes',
                'unit': 'byte',
                'rate': True,
                'retention': 3
            }
        }
    }

    def __init__(self):
        super().__init__(self.definition)
