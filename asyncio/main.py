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

async def glances_stats(plugin, refresh=1):
    plugin.update()
    ret = plugin.stats
    await asyncio.sleep(refresh)
    return ret

async def main():
    name_list = ['cpu', 'percpu', 'mem', 'swap']
    # name_list = ['percpu']
    plugins_list = [getattr(sys.modules[__name__], s) for s in name_list]
    stats_list = [glances_stats(p) for p in plugins_list]
    ret_list = await asyncio.gather(*stats_list)
    pprint.pprint(ret_list)

if __name__ == "__main__":
    start = time.perf_counter()
    for i in range(3):
        asyncio.run(main())
    elapsed = time.perf_counter() - start
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
