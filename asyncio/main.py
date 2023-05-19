#!/usr/bin/env python3

import sys
import time
import asyncio
import pprint

import psutil

from plugin_cpu import cpu
from plugin_percpu import percpu
from plugin_mem import mem
from plugin_swap import swap
from plugin_network import network
from plugin_process import process

async def glances_stats(plugin, refresh=3):
    start = time.perf_counter()
    plugin.update()
    ret = plugin.get
    elapsed = time.perf_counter() - start
    if elapsed > refresh:
        print('WARNING: refresh time is too short ({}s)'.format(elapsed))
    else:
        await asyncio.sleep(refresh - elapsed)
    return ret

async def main():
    name_list = ['cpu', 'percpu', 'mem', 'swap', 'network', 'process']
    # name_list = ['process']
    plugins_list = [getattr(sys.modules[__name__], s) for s in name_list]
    stats_list = [glances_stats(p) for p in plugins_list]
    ret_list = await asyncio.gather(*stats_list)
    for ret in ret_list:
        print(ret['stats'])
        print(ret['view'])
        print(ret['view_curses'])
        print()

if __name__ == "__main__":
    while True:
        start = time.perf_counter()
        asyncio.run(main())
        elapsed = time.perf_counter() - start
        print(f"{__file__} executed in {elapsed:0.2f} seconds.")
