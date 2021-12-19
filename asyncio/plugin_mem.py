#!/usr/bin/env python3

from plugin import GlancesPlugin

class Mem(GlancesPlugin):

    def __init__(self):
        super(Mem, self).__init__()

        # Init the args
        self.args['psutil_fct'] = [{'name': 'virtual_memory'}]

        # Transform the stats
        # Add some derived parameters stats (functions defined below)
        self.args['transform'].update({'derived_parameters': ['free_abc', 'used_abc']})

    ###############################
    # Derived parameters definition
    ###############################

    def free_abc(self):
        # See https://unix.stackexchange.com/questions/65835/htop-reporting-much-higher-memory-usage-than-free-or-top
        # free_abc = available + buffer + cached
        if 'available' in self.stats and self.stats['available'] is not None:
            ret = self.stats.get('available') \
                + self.stats.get('buffers', 0) \
                + self.stats.get('cached', 0)
        else:
            ret = None
        return ret

    def used_abc(self):
        # See https://unix.stackexchange.com/questions/65835/htop-reporting-much-higher-memory-usage-than-free-or-top
        # used_abc = total - free_abc
        return self.stats.get('total') - self.stats.get('free_abc')


mem = Mem()
