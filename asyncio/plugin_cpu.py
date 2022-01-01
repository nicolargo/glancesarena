#!/usr/bin/env python3

from plugin import GlancesPlugin

class Cpu(GlancesPlugin):

    """CPU plugin
    Stat example:
    {'cpu_percent': 0.0, 'user': 0.0, 'nice': 0.0, 'system': 0.0, 'idle': 0.0,
     'iowait': 0.0, 'irq': 0.0, 'softirq': 0.0, 'steal': 0.0, 'guest': 0.0,
     'guest_nice': 0.0, 'ctx_switches': 3271803998, 'interrupts': 1205799541,
     'soft_interrupts': 787542175, 'syscalls': 0, 'ctx_switches_rate': None,
     'interrupts_rate': None, 'soft_interrupts_rate': None, 'syscalls_rate': None}
    """

    def __init__(self):
        super(Cpu, self).__init__()

        # Set the PsUtil functions used to grab the stats
        self.args['psutil_fct'] = [{'name': 'cpu_percent', 'args': {'interval': 0.0}},
                                   {'name': 'cpu_times_percent', 'args': {'interval': 0.0}},
                                   {'name': 'cpu_stats'}]

        # Transform the stats
        # Gauge: for each gauge field, create an extra field with the rate per second
        self.args['transform'].update({'gauge': ['ctx_switches', 'interrupts', 'soft_interrupts', 'syscalls']})

        # Init the view layout
        self.args['view_layout'] = {
            'columns': [
                # First column
                {
                    'lines': [['CPU', '{cpu_percent}'],
                              ['user', '{user}'],
                              ['system', '{system}'],
                              ['iowait', '{iowait}']]
                },
                # Second column
                {
                    'lines': [['idle', '{idle}'],
                              ['irq', '{irq}'],
                              ['nice', '{nice}'],
                              ['steal', '{steal}']]
                },
                # Third column
                {
                    'lines': [['ctx_sw', '{ctx_switches}'],
                              ['inter', '{interrupts}'],
                              ['sw_int', '{soft_interrupts}']]
                },
            ]
        }

cpu = Cpu()
