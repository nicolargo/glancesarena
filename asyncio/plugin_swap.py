#!/usr/bin/env python3

from plugin import GlancesPlugin

class Swap(GlancesPlugin):

    def __init__(self):
        super(Swap, self).__init__()

        # Init the args
        self.args['psutil_fct'] = [{'name': 'swap_memory'}]

        # Init the view layout
        self.args['view_layout'] = [# Only one column
                                    {
                                        'lines': [['SWAP', '{percent:>5}'],
                                                  ['total', '{total:>5}'],
                                                  ['used', '{used:>5}'],
                                                  ['free', '{free:>5}']]
                                    }
                                    ]

swap = Swap()
