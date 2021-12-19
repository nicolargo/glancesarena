#!/usr/bin/env python3

from plugin import GlancesPlugin

class Cpu(GlancesPlugin):

    def __init__(self):
        super(Cpu, self).__init__()

        # Set the PsUtil functions used to grab the stats
        self.args['psutil_fct'] = [{'name': 'cpu_percent', 'args': {'interval': 0.0}},
                                   {'name': 'cpu_times_percent', 'args': {'interval': 0.0}},
                                   {'name': 'cpu_stats'}]

        # Transform the stats
        # Gauge: for each gauge field, create an extra field with the rate per second
        self.args['transform'].update({'gauge': ['ctx_switches', 'interrupts', 'soft_interrupts', 'syscalls']})

cpu = Cpu()
