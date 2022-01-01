#!/usr/bin/env python3

from plugin import GlancesPlugin

class Swap(GlancesPlugin):

    """Mem (SWAP) plugin
    Stat example:
    {'total': 8082419712, 'used': 1379536896, 'free': 6702882816,
     'percent': 17.1, 'sin': 2959507456, 'sout': 6242086912}
    """

    def __init__(self):
        super(Swap, self).__init__()

        # Init the args
        self.args['psutil_fct'] = [{'name': 'swap_memory'}]

        # Init the view layout
        self.args['view_layout'] = {
            'columns': [
                # Only one column
                {
                    'lines': [['SWAP', '{percent}%'],
                              ['total', '{total}'],
                              ['used', '{used}'],
                              ['free', '{free}']]
                }
            ]
        }

swap = Swap()
