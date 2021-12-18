#!/usr/bin/env python3

from plugin import GlancesPlugin

class Cpu(GlancesPlugin):

    def __init__(self, args=None):
        super(Cpu, self).__init__(args=args)

        # Init the stats
        self.args['psutil_fct'] = [{'name': 'cpu_times'},
                                   {'name': 'cpu_stats'}]

    def transform(self):
        """Transform the CPU stats."""
        pass

cpu = Cpu()
