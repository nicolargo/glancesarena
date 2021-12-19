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
        if 'available' in self._stats and self._stats['available'] is not None:
            ret = self._stats.get('available') \
                + self._stats.get('buffers', 0) \
                + self._stats.get('cached', 0)
        else:
            ret = None
        return ret

    def used_abc(self):
        # See https://unix.stackexchange.com/questions/65835/htop-reporting-much-higher-memory-usage-than-free-or-top
        # used_abc = total - free_abc
        return self._stats.get('total') - self._stats.get('free_abc')


mem = Mem()
