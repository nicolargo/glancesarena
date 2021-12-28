#!/usr/bin/env python3

from plugin import GlancesPlugin

class Cpu(GlancesPlugin):

    """CPU plugin
    Stats example:
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

        # Init the views
        self.args['view_layout'] = [# First column
                                    {
                                        'width': 12,
                                        'lines': [('CPU', '{cpu_percent:>5}'),
                                                  ('user', '{user:>5}'),
                                                  ('system', '{system:>5}'),
                                                  ('iowait', '{iowait:>5}')]
                                    },
                                    # Second column
                                    {
                                        'width': 12,
                                        'lines': [('idle', '{idle:>5}'),
                                                  ('irq', '{irq:>5}'),
                                                  ('nice', '{nice:>5}'),
                                                  ('steal', '{steal:>5}')]
                                    },
                                    # Third column
                                    {
                                        'width': 12,
                                        'lines': [('ctx_sw', '{ctx_switches:>5}'),
                                                  ('inter', '{interrupts:>5}'),
                                                  ('sw_inter', '{soft_interrupts:>5}')]
                                    },
                                    ]

        # . will be removed (just here to simplify the alignment)
#         self.args['view_template'] = \
# """\
# CPU    {cpu_percent:>5} idle  {idle:>5} ...ctx_sw   {ctx_switches:>5}
# user   {user:>5} .......irq   {softirq:>5} inter    {interrupts:>5}
# system {system:>5} .....nice  {nice:>5} ...sw_inter {soft_interrupts:>5}
# iowait {iowait:>5} .....steal {steal:>5}\
# """.replace('.', '')

cpu = Cpu()
