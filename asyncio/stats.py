#!/usr/bin/env python3

from pydantic.dataclasses import dataclass


@dataclass
class Stats:
    key: str = ''
    stats: dict = {}

