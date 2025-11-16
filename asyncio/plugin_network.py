#!/usr/bin/env python3

from plugin import GlancesPlugin


class Network(GlancesPlugin):
    """Network (interface) plugin
    Stat example:
    [{'bytes_sent': 58292942, 'bytes_recv': 20339125, 'packets_sent': 161827,
      'packets_recv': 28452, 'errin': 0, 'errout': 0, 'dropin': 0, 'dropout': 0,
      'key': 'interface_name', 'interface_name': 'veth2845bac', 'isup': True,
      'duplex': 'FULL', 'speed': 10485760000, 'mtu': 1500, 'bytes_recv_rate': 0.0,
      'bytes_sent_rate': 0.0, 'cumulative_cx': 78742607, 'cumulative_cx_rate': 0.0}, ... ]
    """

    def __init__(self):
        super(Network, self).__init__()

        # Set the PsUtil functions used to grab the stats
        # net_io_counters(pernic=True)
        self.stats_def["psutil_fct"] = [
            {
                "name": "net_io_counters",
                "args": {"pernic": True},
                "key": "interface_name",
            },
            {"name": "net_if_stats", "key": "interface_name"},
        ]

        # Transform the stats
        # Gauge: for each gauge field, create an extra field with the rate per second
        self.stats_def["transform"].update({"gauge": ["bytes_recv", "bytes_sent"]})
        # Add some derived parameters stats (functions defined below)
        self.stats_def["transform"].update(
            {
                "derived_parameters": [
                    "speed",
                    "duplex",
                    "cumulative_cx",
                    "cumulative_cx_rate",
                ]
            }
        )

        # Init the view layout
        self.stats_def["view_layout"] = {
            # We will iterate the second line (index of first line is 0)
            "line_to_iter": 1,
            "columns": [
                # First column
                {"lines": [["NETWORK"], ["{interface_name}"]]},
                # Second column
                {"lines": [["Rx/s"], ["{bytes_recv_rate}"]]},
                # Third column
                {"lines": [["Tx/s"], ["{bytes_sent_rate}"]]},
            ],
        }

    ###############################
    # Derived parameters definition
    ###############################

    def speed(self):
        """Interface speed in Mbps, convert it to bps
        Can be always 0 on some OSes"""
        return [i["speed"] * 1048576 if "speed" in i else "-" for i in self.stats]

    def duplex(self):
        """Interface mode
        See documentation here: https://psutil.readthedocs.io/en/latest/#psutil.net_if_stats"""
        return [
            str(i["duplex"]).split("_")[-1] if "duplex" in i else "-"
            for i in self.stats
        ]

    def cumulative_cx(self):
        """Rx+Tx"""
        return [i["bytes_recv"] + i["bytes_sent"] for i in self.stats]

    def cumulative_cx_rate(self):
        """Rx+Tx rate"""
        return [
            i["bytes_recv_rate"] + i["bytes_sent_rate"]
            if i["bytes_recv_rate"] is not None
            else 0
            for i in self.stats
        ]


network = Network()
