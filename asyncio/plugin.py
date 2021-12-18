#!/usr/bin/env python3

import psutil

class GlancesPlugin(object):

    def __init__(self, args=None):
        """Init the plugin."""
        # Init args (self.args)
        self.init_args(args)
        # Init stats (self._stats)
        self.reset()

    def init_args(self, args=None):
        """Init the args of the plugin."""
        # Argument init
        if args is None:
            self.args = {}
        else:
            self.args = args

    def reset(self):
        """Reset/init the stats."""
        self._stats = None

    @property
    def stats(self):
        return self._stats

    def update(self):
        self.grab()
        self.add_metadata()
        self.transform()

    def grab(self):
        """Grab the stats."""
        # Grab the stats using the psutil_fct list provided by the plugin
        # The psutil_fct list is a list of dictionaries with the following format:
        # - name key: psutil function to call
        # - args key: psutil arguments of the function (optional)
        if 'psutil_fct' not in self.args:
            return

        stats = None
        for psutil_fct in self.args['psutil_fct']:
            # Get the PsUtil function name and args
            psutil_fct_name = psutil_fct['name']
            psutil_fct_args = psutil_fct.get('args', {})
            if psutil_fct_name in dir(psutil):
                # The PsUtil function is available
                # Grab the PsUtil stats
                psutil_stats = getattr(psutil, psutil_fct_name)(**psutil_fct_args)
                # Convert in a standard object (dict or list of dict)
                if psutil_stats is None:
                    # TODO: log error
                    pass
                elif isinstance(psutil_stats, list):
                    psutil_stats = [s._asdict() if (s is not None and hasattr(s, '_asdict')) else None for s in psutil_stats]
                elif hasattr(psutil_stats, '_asdict'):
                    psutil_stats = psutil_stats._asdict()
                # Update the stats
                if stats is None:
                    stats = psutil_stats
                elif isinstance(stats, dict):
                    stats.update(psutil_stats)
                elif isinstance(stats, list):
                    stats += psutil_stats

        self._stats = stats
        return self._stats

    def add_metadata(self):
        """Add metadata to stats."""
        pass

    def transform(self):
        """Transform the stats."""
        pass
