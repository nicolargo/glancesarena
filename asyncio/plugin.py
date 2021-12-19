#!/usr/bin/env python3

import time

import psutil

class GlancesPlugin(object):

    def __init__(self):
        """Init the plugin."""
        # Init args (self.args)
        self.init_args()

        # Init the main plugin object
        # It's a dictionary
        self._object = {
            'name': self.__class__.__name__,
            'stats': None,
            'time_since_update': None
        }
        self._last_update_time = None

        # Init the stats (self._stats)
        self.reset()

    def init_args(self):
        """Init the args."""
        # Set the default values
        self.args = {
            'psutil_fct': [],
            'transform': {
                'gauge': [],
                'derived_parameters': []
            }
        }

    def reset(self):
        """Reset/init the stats."""
        self._stats = None
        self._stats_previous = None

    @property
    def stats(self):
        return self._object

    def update(self):
        self._stats_previous = self._stats
        self.grab_stats()
        self.add_metadata()
        self.transform()
        self.add_stats()

    def grab_stats(self):
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
                    psutil_stats = [s._asdict() if (s is not None and hasattr(s, '_asdict')) else {psutil_fct_name: s} for s in psutil_stats]
                elif hasattr(psutil_stats, '_asdict'):
                    psutil_stats = psutil_stats._asdict()
                else:
                    psutil_stats = {psutil_fct_name: psutil_stats}

                # Update the stats
                if isinstance(stats, dict):
                    # It's a dict
                    # Merge the PsUtil stats with the existing stats
                    stats.update(psutil_stats)
                elif isinstance(stats, list):
                    # It's a list of dict
                    # Merge dicts in the list
                    if stats == []:
                        stats += psutil_stats
                    else:
                        for i in range(len(stats)):
                            stats[i].update(psutil_stats[i])
                else:
                    # Others cases...
                    # Just copy the PsUtil stats to the existing stats
                    stats = psutil_stats

        self._stats = stats
        return self._stats

    def add_metadata(self):
        """Add metadata to the global object."""
        # Add time since last update
        current_time = time.time()
        if self._last_update_time is None:
            self._object['time_since_update'] = None
        else:
            self._object['time_since_update'] = current_time - self._last_update_time
        self._last_update_time = current_time

    def transform(self):
        """Transform the stats."""
        self._transform_gauge()
        self._derived_parameters()

    def _transform_gauge(self):
        """Tranform gauge to rate."""
        if 'transform' in self.args and 'gauge' in self.args['transform']:
            for key in self.args['transform']['gauge']:
                if key in  self._stats and self._object['time_since_update'] is not None:
                    self._stats[key + '_rate'] = (self._stats[key] - self._stats_previous[key]) / self._object['time_since_update']
                else:
                    self._stats[key + '_rate'] = None

    def _derived_parameters(self):
        """Add dervied parameters to the self._stats from the self._stats."""
        if 'transform' in self.args and 'derived_parameters' in self.args['transform']:
            for key in self.args['transform']['derived_parameters']:
                if hasattr(self, key):
                    self._stats[key] = getattr(self, key)()

    def add_stats(self):
        """Update stats in the global object."""
        self._object['stats'] = self._stats
