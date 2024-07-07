#!/usr/bin/env python3

import psutil
from plugin import GlancesPlugin


class Process(GlancesPlugin):
    """Process plugin
    Stat example:
    """

    def __init__(self):
        super(Process, self).__init__()

        # Init the args
        self.args["glances_fct"] = [{"name": "process_list"}]

        # Transform the stats
        self.args["transform"].update({"expand": ["memory_info"]})
        self.args["transform"].update({"remove": ["memory_info"]})

        # Init the view layout
        self.args["view_layout"] = {
            "line_to_iter": 1,
            "no_format": ["pid"],
            "columns": [
                # First column
                {"lines": [["CPU%"], ["{cpu_percent}"]]},
                # Second column
                {"lines": [["MEM%"], ["{memory_percent}"]]},
                # Third column
                {"lines": [["VIRT"], ["{vms}"]]},
                # Fourth column
                {"lines": [["RES"], ["{rss}"]]},
                # Fifth column
                {"lines": [["PID"], ["{pid}"]]},
                # Sixth column
                {"lines": [["USER"], ["{username}"]]},
                # Last column
                {"lines": [["command"], ["{name}"]]},
            ],
        }

    ###############################
    # Glances internal functions
    ###############################

    def process_list(self):
        """Return the processlist"""
        sorted_attrs = [
            "cpu_percent",
            # 'cpu_times',
            "memory_percent",
            "name",
            "status",
            # 'num_threads'
        ]
        displayed_attr = ["memory_info", "nice", "pid", "ppid"]
        cached_attrs = ["cmdline", "username"]
        return [
            p.as_dict(attrs=sorted_attrs + displayed_attr + cached_attrs)
            for p in psutil.process_iter(attrs=None, ad_value=None)
        ]

    def memory_info(self):
        ret = []
        for p in self._stats:
            if "memory_info" in p:
                ret.append(p["memory_info"]._asdict())
        return ret


process = Process()
