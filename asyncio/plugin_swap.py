#!/usr/bin/env python3

from plugin import GlancesPlugin

class Swap(GlancesPlugin):

    def __init__(self):
        super(Swap, self).__init__()

        # Init the args
        self.args['psutil_fct'] = [{'name': 'swap_memory'}]

        # Init the views
        self.args['view_template'] = \
"""\
SWAP {percent}
total {total}
used {used}
free {free}\
"""

swap = Swap()
