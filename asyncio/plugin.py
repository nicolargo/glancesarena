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
            'view_layout': {}
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
        # Stats
        #######

        # Store the old stat values in order to compute rates
        self._stats_previous = self._stats

        # Stats ET(not L)
        self.grab_stats()
        self.add_metadata()
        self.transform()

        # Stats (not ET)L
        self.add_stats()

        # Views
        #######
        # @TODO: not sure this is the good place for this call
        self.update_view()

    def grab_stats(self):
        """Grab the stats."""

        # Using PsUtil functions
        self._grab_psutil_stats()

        # Using Glances (internals) functions
        self._grab_glances_stats()

        return self._stats

    def _grab_psutil_stats(self):
        """Grab the stats using the psutil_fct list provided by the plugin.
           The psutil_fct list is a list of dictionaries with the following format:
           - name key: psutil function to call
           - args key: psutil arguments of the function (optional)"""

        if 'psutil_fct' not in self.args:
            return False

        for psutil_fct in self.args['psutil_fct']:
            # Get the PsUtil function name and args
            psutil_fct_name = psutil_fct['name']
            psutil_fct_args = psutil_fct.get('args', {})

            if psutil_fct_name not in dir(psutil):
                # @TODO: add a logger (psutil fct do not exist or being supported)
                continue

            # The PsUtil function is available
            # Execute it
            psutil_stats = getattr(psutil, psutil_fct_name)(**psutil_fct_args)

            # Convert in a standard object (dict or list of dict)
            if psutil_stats is None:
                # TODO: log error
                pass
            elif isinstance(psutil_stats, list):
                # The PsUtil return a list, convert result to a list of dict (if possible)
                psutil_stats = [s._asdict() if (s is not None and hasattr(s, '_asdict')) else {psutil_fct_name: s} for s in psutil_stats]
            elif hasattr(psutil_stats, '_asdict'):
                # The PsUtil can return a dict representation, use it
                psutil_stats = psutil_stats._asdict()
            else:
                if 'key' in psutil_fct:
                    # A key is provided, use the PsUtil dict key as stat key
                    # and add the 'key' field (content the key value)
                    # Ex: For Network, 'key' = 'interface_name', 'interface_name': 'eth0'
                    stats_temp = []
                    for k, v in psutil_stats.items():
                        value_temp = v._asdict()
                        value_temp['key'] = psutil_fct['key']
                        value_temp[psutil_fct['key']] = k
                        stats_temp.append(value_temp)
                    psutil_stats = stats_temp
                else:
                    psutil_stats = {psutil_fct_name: psutil_stats}

            # Update the stats
            self._merge_into_stats(psutil_stats)

        return True

    def _grab_glances_stats(self):
        """Grab the stats using the glances_fct list provided by the plugin.
           The glances_fct list is a list of dictionaries with the following format:
           - name key: Glances function to call
           - args key: Glances arguments of the function (optional)"""

        if 'glances_fct' not in self.args:
            return False

        for glances_fct in self.args['glances_fct']:
            # Get the PsUtil function name and args
            glances_fct_name = glances_fct['name']
            glances_fct_args = glances_fct.get('args', {})

            if glances_fct_name not in dir(self):
                # @TODO: add a logger (Glances fct do not exist)
                raise("Glances function {} not found".format(glances_fct_name))

            # The Glances function is available
            # Execute it
            glances_stats = getattr(self, glances_fct_name)(**glances_fct_args)

            # Update the stats
            self._merge_into_stats(glances_stats)

        return True

    def _merge_into_stats(self, new_stat):
        """Merge new_stats into self._stats."""
        # Update the stats
        if isinstance(self._stats, dict):
            # It's a dict
            # Merge the PsUtil stats with the existing stats
            # So only one dict will be returned
            self._stats.update(new_stat)
        elif isinstance(self._stats, list):
            # It's a list of dict
            #
            if self._stats == []:
                self._stats += new_stat
            else:
                for i in range(len(self._stats)):
                    # @TODO: some time we have the following error with the Process class
                    # File "/home/nicolargo/dev/glancesarena/asyncio/plugin.py", line 163, in _grab_glances_stats
                    # self._merge_into_stats(glances_stats)
                    # File "/home/nicolargo/dev/glancesarena/asyncio/plugin.py", line 182, in _merge_into_stats
                    # self._stats[i].update(new_stat[i])
                    # IndexError: list index out of range
                    # make: *** [Makefile:22: run-asyncio] Error 1
                    self._stats[i].update(new_stat[i])

        else:
            # Others cases...
            # Just copy the PsUtil stats to the existing stats
            self._stats = new_stat

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
        # Compute rate
        self._transform_gauge()
        # Expand some parameters
        self._expand_parameters()
        # Evaluate all derived parameters
        self._derived_parameters()
        # Remove unused stats
        self._remove_parameters()

    def _transform_gauge(self):
        """Tranform gauge to rate."""
        if 'transform' not in self.args or 'gauge' not in self.args['transform']:
            return
        for key in self.args['transform']['gauge']:
            if isinstance(self._stats, list):
                for count, stat in enumerate(self._stats):
                    if key in stat and self._object['time_since_update'] is not None:
                        stat[key + '_rate'] = (stat[key] - self._stats_previous[count].get(key, stat[key])) / self._object['time_since_update']
                    else:
                        stat[key + '_rate'] = None
            elif isinstance(self._stats, dict):
                if key in self._stats and self._object['time_since_update'] is not None:
                    self._stats[key + '_rate'] = (self._stats[key] - self._stats_previous.get(key, self._stats[key])) / self._object['time_since_update']
                else:
                    self._stats[key + '_rate'] = None

    def _derived_parameters(self):
        """Add derived parameters to the self._stats."""
        if 'transform' in self.args and 'derived_parameters' in self.args['transform']:
            for key in self.args['transform']['derived_parameters']:
                if isinstance(self._stats, list):
                    dp = getattr(self, key)()
                    for count, stat in enumerate(self._stats):
                         stat[key] = dp[count]
                elif isinstance(self._stats, dict):
                    if hasattr(self, key):
                        self._stats[key] = getattr(self, key)()

    def _expand_parameters(self):
        """Expand parameters."""
        if 'transform' in self.args and 'expand' in self.args['transform']:
            for key in self.args['transform']['expand']:
                if isinstance(self._stats, list):
                    ep = getattr(self, key)()
                    for count, stat in enumerate(self._stats):
                         stat.update(ep[count])
                elif isinstance(self._stats, dict):
                    if hasattr(self, key):
                        self._stats.update(getattr(self, key)())

    def _remove_parameters(self):
        """Remove unused parameters"""
        if 'transform' in self.args and 'remove' in self.args['transform']:
            for key in self.args['transform']['remove']:
                if isinstance(self._stats, list):
                    for stat in self._stats:
                        if key in stat:
                            del stat[key]
                elif isinstance(self._stats, dict):
                    if key in self._stats:
                        del self._stats[key]

    def add_stats(self):
        """Update stats in the global object."""
        self._object['stats'] = self._stats

    def update_view(self):
        """Update the view with the stats."""
        # There is a layout, use it to build all others views
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
        if 'view_layout' not in self.args or self.args['view_layout'] == {}:
            return

        # Convert the stats to "human reading" unit
        stats_human = build_stats_human(self._stats, self.args['view_layout'])

        # We build the view
        view = []

        # Layout (columns) to view (lines)
        max_lines = max([len(column['lines']) for column in self.args['view_layout']['columns'] if 'lines' in column])
        for line_nb in range(max_lines):
            if 'line_to_iter' in self.args['view_layout'] and line_nb == self.args['view_layout']['line_to_iter']:
                for stat_human in stats_human:
                    line = build_line(self.args['view_layout']['columns'],
                                    line_nb,
                                    stat_human)
                    view.append(line)
            else:
                line = build_line(self.args['view_layout']['columns'],
                                  line_nb,
                                  stats_human[0])
                view.append(line)

        # Compute padding
        set_line_padding(view)

        # Update the plugin's object
        self._object['view'] = view

    def view_to_curses(self, space_between_columns=1):
        """Convert the layout to a view (mother for all king of views)."""
        self._object['view_curses'] = ''

        if not self._object['view']:
            return

        for line in self._object['view']:
            for count, raw in enumerate(line['raw']):
                self._object['view_curses'] += '{raw:{fill}{align}{padding}}'.format(raw=raw,
                                                                                     fill=' ',
                                                                                     align=line['align'][count],
                                                                                     padding=line['padding'][count])
                if count != len(line['raw']) - 1:
                    self._object['view_curses'] += ' ' * space_between_columns
            self._object['view_curses'] += '\n'


def build_stats_human(stats, layout):
    """Return human representation of stats"""
    ret = []
    no_format = layout['no_format'] if 'no_format' in layout else []
    if isinstance(stats, list):
        for i in stats:
            ret.append({k: (auto_unit(v) if k not in no_format else v) for k, v in i.items()})
    elif isinstance(stats, dict):
        ret.append({k: (auto_unit(v) if k not in no_format else v) for k, v in stats.items()})
    else:
        raise ValueError("stats should be list or dict (got {})".format(type(stats)))
    return ret


def build_line(columns, line_nb, stats_human):
    """Build the view for the line_nb getting stats in the stats_human"""
    line = {
        'raw': [],
        'align': [],
        'padding': []
    }
    for column in columns:
        if line_nb > len(column['lines']) - 1:
            # No more stats for this column
            continue
        line['raw'].extend(build_raw_view(column['lines'][line_nb],
                                          stats_human))
        line['align'].extend(build_align_view(column['lines'][line_nb]))
    return line


def set_line_padding(view):
    """Set the padding of each fields"""
    fields_size = [[len(i) for i in l['raw']] for l in view]
    fields_padding = [max([c[i] for c in fields_size if len(c) > i ]) for i in range(len(fields_size[0]))]
    for line in view:
        line['padding'] = fields_padding


def build_raw_view(lines_layout, stats_human, no_stat_human='-'):
    """Convert the lines_layout to human reading stats list"""
    raw = []
    for v in lines_layout:
        try:
            raw.append(v.format(**stats_human))
        except KeyError:
            raw.append(no_stat_human)
    return raw


def build_align_view(lines_layout):
    """Convert the lines_layout to alignement list (for UI)"""
    return ['<' if c == 0 else '>' for c, _ in enumerate(lines_layout)]


def auto_unit(number,
              low_precision=True,
              min_symbol='K',
              none_representation='-'):
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
    :none_representation: what is returned if number is None
    """
    if number == 0:
        return '0'
    elif number is None:
        return none_representation
    elif isinstance(number, str) or not isinstance(number, (int, float)):
        return number

    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    if min_symbol in symbols:
        symbols = symbols[symbols.index(min_symbol):]
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

    decimal_precision = 1 if low_precision else 2
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
            return '{:.{decimal}f}{symbol}'.format(value,
                                                   decimal=decimal_precision,
                                                   symbol=symbol)
    return '{:.{decimal}f}{symbol}'.format(value if number > 1024 else number,
                                           decimal=decimal_precision,
                                           symbol='')
