#!/usr/bin/env python3

import time

import psutil

class GlancesPlugin(object):

    def __init__(self):
        """Init the plugin."""
        # Init args (self.args)
        self.init_args()

        # Init the stats (self._stats)
        self.reset_stats()

        # Init the main sbject (self._object)
        self.init_object()

    def init_args(self):
        """Init the args."""
        # Set the default values
        self.args = {
            'psutil_fct': [],
            'transform': {
                'gauge': [],
                'derived_parameters': []
            },
            'view_layout': [],
            'view_template': ''
        }

    def reset_stats(self):
        """Reset/init the stats."""
        self._stats = None

    def init_object(self):
        """Init the global object."""
        # It's a dictionary
        self._object = {
            'name': self.__class__.__name__,
            'stats': None,
            'view': None,
            'view_curses': None,
            'time_since_update': None
        }
        # Only used to compute time_since_update
        self._last_update_time = None

    @property
    def get(self):
        return self._object

    @property
    def stats(self):
        return self._stats

    def update(self):
        self._stats_previous = self._stats

        # Stats
        #######
        # Stats ET(not L)
        self.grab_stats()
        self.add_metadata()
        self.transform()
        # Stats (not ET)L
        self.add_stats()

        # Views
        #######
        self.update_view()

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

    def update_view(self):
        """Update the view with the stats."""
        # There is a layout, use it to build all others views
        if 'view_layout' in self.args:
            self.layout_to_view()

        # Update the curses view
        self.view_to_curses()

    def layout_to_view(self):
        """Convert the layout to a view (mother for all king of views).
        Layout:
            A layout is a list of columns (dict).
            A column is composed of lines (list of list).
            A column may contain is width and is lenght.
        View:
            A view is a list of lines (dict)
            A line is...
        """
        stats_human = {k: auto_unit(v) for k, v in self._stats.items()}
        self._object['view'] = self.args['view_layout']
        for column in self._object['view']:
            for line in column['lines']:
                # Replace layout value by the current value
                line[1] = line[1].format(**stats_human)
            if 'lenght' not in column:
                # lenght is not provided, compute it
                column['lenght'] = len(column['lines'])
            if 'width' not in column:
                # Width is not provided, compute it
                column['width'] = max([len(' '.join(line)) for line in column['lines']])

    def view_to_curses(self):
        """Convert the layout to a view (mother for all king of views)."""
        self._object['view_curses'] = ''
        lines_number = max([len(i['lines']) for i in self._object['view'] if 'lines' in i])
        for line in range(lines_number):
            first_column = True
            for column in self._object['view']:
                if line > len(column['lines']) - 1:
                    # No more stats for this column
                    continue
                # Manage space between columns
                if not first_column:
                    self._object['view_curses'] += ' '
                else:
                    first_column = False
                # Add lines
                label = column['lines'][line][0]
                value = column['lines'][line][1]
                label_width = column['width'] - len(value) + 1
                self._object['view_curses'] += '{label:{fill}{align}{width}}{value}'.format(label=label,
                                                                                            fill=' ',
                                                                                            align='<',
                                                                                            width=label_width,
                                                                                            value=value)
            self._object['view_curses'] += '\n'


def auto_unit(number, low_precision=False, min_symbol='K', none_representation='-'):
    """Make a nice human-readable string out of number.
    Number of decimal places increases as quantity approaches 1.
    CASE: 613421788        RESULT:       585M low_precision:       585M
    CASE: 5307033647       RESULT:      4.94G low_precision:       4.9G
    CASE: 44968414685      RESULT:      41.9G low_precision:      41.9G
    CASE: 838471403472     RESULT:       781G low_precision:       781G
    CASE: 9683209690677    RESULT:      8.81T low_precision:       8.8T
    CASE: 1073741824       RESULT:      1024M low_precision:      1024M
    CASE: 1181116006       RESULT:      1.10G low_precision:       1.1G
    :low_precision: returns less decimal places potentially (default is False)
                    sacrificing precision for more readability.
    :min_symbol: Do not approach if number < min_symbol (default is K)
    """
    if number is None:
        return none_representation
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    if min_symbol in symbols:
        symbols = symbols[symbols.index(min_symbol) :]
    prefix = {
        'Y': 1208925819614629174706176,
        'Z': 1180591620717411303424,
        'E': 1152921504606846976,
        'P': 1125899906842624,
        'T': 1099511627776,
        'G': 1073741824,
        'M': 1048576,
        'K': 1024,
    }

    for symbol in reversed(symbols):
        value = float(number) / prefix[symbol]
        if value > 1:
            decimal_precision = 0
            if value < 10:
                decimal_precision = 2
            elif value < 100:
                decimal_precision = 1
            if low_precision:
                if symbol in 'MK':
                    decimal_precision = 0
                else:
                    decimal_precision = min(1, decimal_precision)
            elif symbol in 'K':
                decimal_precision = 0
            return '{:.{decimal}f}{symbol}'.format(value, decimal=decimal_precision, symbol=symbol)
    return '{!s}'.format(number)
