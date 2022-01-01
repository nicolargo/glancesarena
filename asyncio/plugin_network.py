#!/usr/bin/env python3

from plugin import GlancesPlugin

class Network(GlancesPlugin):

    """Network (interface) plugin
    Stats example:
    """

    def __init__(self):
        super(Network, self).__init__()

        # Set the PsUtil functions used to grab the stats
        # net_io_counters(pernic=True)
        self.args['psutil_fct'] = [{'name': 'net_io_counters',
                                    'args': {'pernic': True},
                                    'key': 'interface_name'},
                                   {'name': 'net_if_stats',
                                    'key': 'interface_name'}]

        # Transform the stats
        # Gauge: for each gauge field, create an extra field with the rate per second
        self.args['transform'].update({'gauge': ['bytes_recv', 'bytes_sent']})
        # Add some derived parameters stats (functions defined below)
        self.args['transform'].update({'derived_parameters': ['speed', 'duplex']})

        # Init the view layout
        self.args['view_layout'] = {
            # We will iterate the second line (index of first line is 0)
            'line_to_iter': 1,
            'columns': [
                # First column
                {
                    'lines': [['NETWORK'],
                              ['{interface_name}']]
                },
                # Second column
                {
                    'lines': [['Rx/s'],
                              ['{bytes_recv_rate}']]
                },
                # Third column
                {
                    'lines': [['Tx/s'],
                              ['{bytes_sent_rate}']]
                }
            ]
        }

    ###############################
    # Derived parameters definition
    ###############################

    def speed(self):
        """Interface speed in Mbps, convert it to bps
        Can be always 0 on some OSes"""
        return [s['speed'] * 1048576 if 'speed' in s else '-' for s in self.stats]


    def duplex(self):
        """Interface mode
        See documentation here: https://psutil.readthedocs.io/en/latest/#psutil.net_if_stats"""
        return [str(s['duplex']).split('_')[-1] if 'duplex' in s else '-' for s in self.stats]

network = Network()
