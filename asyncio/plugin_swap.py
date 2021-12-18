#!/usr/bin/env python3

from plugin import GlancesPlugin

class Swap(GlancesPlugin):

    def __init__(self, args=None):
        super(Swap, self).__init__(args=args)

        # Init the args
        self.args['psutil_fct'] = [{'name': 'swap_memory'}]

swap = Swap()
