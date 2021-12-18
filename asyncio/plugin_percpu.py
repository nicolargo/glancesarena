#!/usr/bin/env python3

from plugin import GlancesPlugin

class PerCpu(GlancesPlugin):

    def __init__(self, args=None):
        super(PerCpu, self).__init__(args=args)

        # Init the stats
        self.args['psutil_fct'] = [{'name': 'cpu_times',
                                    'args': {'percpu': True}},
                                   {'name': 'cpu_stats'}]

    def transform(self):
        """Transform the CPU stats."""
        pass

percpu = PerCpu()
