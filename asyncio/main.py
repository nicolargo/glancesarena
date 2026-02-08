#!/usr/bin/env python3

import asyncio
import sys
import time

import psutil
from plugin_cpu import cpu
from plugin_mem import mem
from plugin_network import network
from plugin_percpu import percpu
from plugin_process import process
from plugin_swap import swap


async def glances_stats(plugin, refresh=2):
    """Collect stats for a single plugin, respecting the refresh interval."""
    start = time.perf_counter()
    await plugin.update()
    ret = plugin.get
    elapsed = time.perf_counter() - start
    if elapsed > refresh:
        print('WARNING: {} refresh too slow ({:.2f}s > {}s)'.format(
            ret['name'], elapsed, refresh))
    else:
        await asyncio.sleep(refresh - elapsed)
    return ret


async def main():
    """Run one collection cycle: all plugins collect in parallel."""
    # name_list = ['cpu', 'percpu', 'mem', 'swap', 'network', 'process']
    name_list = ['cpu', 'network']
    plugins_list = [getattr(sys.modules[__name__], s) for s in name_list]
    stats_list = [glances_stats(p) for p in plugins_list]
    ret_list = await asyncio.gather(*stats_list)
    for ret in ret_list:
        print(ret['stats'])
        # print(ret['view'])
        # print(ret['view_curses'])
        print()


async def run_forever():
    """Persistent event loop — avoids recreating the loop each cycle."""
    while True:
        start = time.perf_counter()
        await main()
        elapsed = time.perf_counter() - start
        print(f"{__file__} executed in {elapsed:0.2f} seconds.")


if __name__ == "__main__":
    asyncio.run(run_forever())
