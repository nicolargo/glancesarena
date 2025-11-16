#!/usr/bin/env python3

from plugin import GlancesPlugin


class Mem(GlancesPlugin):
    """Mem (RAM) plugin
    Stat example:
    {'total': 7849021440, 'available': 1066557440, 'percent': 86.4,
     'used': 5848440832, 'free': 159309824, 'active': 5579571200,
     'inactive': 1299025920, 'buffers': 420143104, 'cached': 1421127680,
     'shared': 622452736, 'slab': 500400128, 'free_abc': 2907828224,
     'used_abc': 4941193216}
    """

    def __init__(self):
        super(Mem, self).__init__()

        # Init the args
        self.stats_def["psutil_fct"] = [{"name": "virtual_memory"}]

        # Transform the stats
        # Add some derived parameters stats (functions defined below)
        self.stats_def["transform"].update({"derived_parameters": ["free_abc", "used_abc"]})

        # Init the view layout
        self.stats_def["view_layout"] = {
            "columns": [
                # First column
                {
                    "lines": [
                        ["MEM", "{percent}%"],
                        ["total", "{total}"],
                        ["used", "{used_abc}"],
                        ["free", "{free_abc}"],
                    ]
                },
                # Second column
                {
                    "lines": [
                        ["active", "{active}"],
                        ["inactive", "{inactive}"],
                        ["buffer", "{buffers}"],
                        ["cached", "{cached}"],
                    ]
                },
            ]
        }

    ###############################
    # Derived parameters definition
    ###############################

    def free_abc(self):
        # See https://unix.stackexchange.com/questions/65835/htop-reporting-much-higher-memory-usage-than-free-or-top
        # free_abc = available + buffer + cached
        if "available" in self.stats and self.stats["available"] is not None:
            ret = (
                self.stats.get("available")
                + self.stats.get("buffers", 0)
                + self.stats.get("cached", 0)
            )
        else:
            ret = None
        return ret

    def used_abc(self):
        # See https://unix.stackexchange.com/questions/65835/htop-reporting-much-higher-memory-usage-than-free-or-top
        # used_abc = total - free_abc
        return self.stats.get("total") - self.stats.get("free_abc")


mem = Mem()
