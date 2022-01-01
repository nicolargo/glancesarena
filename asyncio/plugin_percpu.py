#!/usr/bin/env python3

from plugin import GlancesPlugin

class PerCpu(GlancesPlugin):

    """CPU (per) plugin
    Stat example:
    [{'cpu_percent': 14.9, 'user': 13.9, 'nice': 0.0, 'system': 1.0,
      'idle': 85.1, 'iowait': 0.0, 'irq': 0.0, 'softirq': 0.0,
      'steal': 0.0, 'guest': 0.0, 'guest_nice': 0.0}, ... ]
    """

    def __init__(self):
        super(PerCpu, self).__init__()

        # Init the stats
        self.args['psutil_fct'] = [{'name': 'cpu_percent', 'args': {'percpu': True, 'interval': 0.0}},
                                   {'name': 'cpu_times_percent', 'args': {'percpu': True, 'interval': 0.0}}]

        # Init the view layout
        # user system   idle iowait  steal
        self.args['view_layout'] = {
            # We will iterate the second line (index of first line is 0)
            'line_to_iter': 1,
            'columns': [
                # First column
                {
                    'lines': [['user'],
                              ['{user}']],
                },
                # Second column
                {
                    'lines': [['system'],
                              ['{system}']],
                },
                # Third column
                {
                    'lines': [['idle'],
                              ['{idle}']],
                },
                # Fourth column
                {
                    'lines': [['iowait'],
                              ['{iowait}']],
                },
                # Fifth column
                {
                    'lines': [['steal'],
                              ['{steal}']],
                }
            ]
        }

percpu = PerCpu()
