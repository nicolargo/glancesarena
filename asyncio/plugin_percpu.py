#!/usr/bin/env python3

from plugin import GlancesPlugin

class PerCpu(GlancesPlugin):

    def __init__(self):
        super(PerCpu, self).__init__()

        # Init the stats
        self.args['psutil_fct'] = [{'name': 'cpu_percent', 'args': {'percpu': True, 'interval': 0.0}},
                                   {'name': 'cpu_times_percent', 'args': {'percpu': True, 'interval': 0.0}}]

percpu = PerCpu()
