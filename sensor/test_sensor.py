#!/usr/bin/env python3

from sensor import Sensor

if __name__ == "__main__":
    sensor = Sensor('test')
    sensor.value = 1
    print(sensor)
