#!/usr/bin/env python3

from datetime import datetime

STATUS_INIT = 0
STATUS_PROCESSED = 1
STATUS_OBSOLETE = 2

class Sensor(object):
    """This class describes a sensor.
    A sensor is defined by:
    - a name
    - a value
    - an unit
    - a description
    - a status
    - an history
    """

    def __init__(self, name, value=None, unit=None, description=None,
                 status=STATUS_INIT, history=[], history_max_size=2):
        self._name = name
        self._value = value
        self._unit = unit
        self._description = description
        self._status = status
        self._history = history
        self._history_max_size = history_max_size
        self._timestamp = datetime.now()

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__repr__())

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._status = STATUS_PROCESSED
        self._timestamp = datetime.now()
        self._value = value
