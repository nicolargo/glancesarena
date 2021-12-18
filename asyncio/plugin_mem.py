#!/usr/bin/env python3

from plugin import GlancesPlugin

class Mem(GlancesPlugin):

    def __init__(self, args=None):
        super(Mem, self).__init__(args=args)

        # Init the args
        self.args['psutil_fct'] = [{'name': 'virtual_memory'}]

mem = Mem()
