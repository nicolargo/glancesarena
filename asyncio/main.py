#!/usr/bin/env python3


import sys
import time
import asyncio

import psutil

async def cpu(refresh=1):
    ret = psutil.cpu_times()
    await asyncio.sleep(refresh)
    return ret

async def mem(refresh=1):
    ret = psutil.virtual_memory()
    await asyncio.sleep(refresh)
    return ret

async def load(refresh=1):
    ret = psutil.getloadavg()
    await asyncio.sleep(refresh)
    return ret

async def main():
    stats_list = ['cpu', 'mem', 'load']
    fct_list = [getattr(sys.modules[__name__], s)() for s in stats_list]
    ret_list = await asyncio.gather(*fct_list)
    print(ret_list)

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - start
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
