# Code from docs.python.org
# https://docs.python.org/ko/3/library/asyncio-eventloop.html

import timeit
import asyncio
import concurrent.futures


def blocking_io():
    # File operations (such as logging) can block the
    # event loop: run them in a thread pool.
    with open("/dev/urandom", "rb") as f:
        return f.read(100)


def cpu_bound():
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a
    # process pool.
    return sum(i * i for i in range(10 ** 7))


async def main():

    loop = asyncio.get_running_loop()
    start = timeit.default_timer()

    ## Options:

    # 1. Run in the default loop's executor:
    result = await loop.run_in_executor(None, cpu_bound)
    print("default thread pool", result)

    # 2. Run in a custom thread pool:
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cpu_bound)
        print("custom thread pool", result)

    # 3. Run in a custom process pool:
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cpu_bound)
        print("custom process pool", result)

    duration = timeit.default_timer() - start
    print("Total Running Time : ", duration)


asyncio.run(main())

#### Result ####
#
# 0.7881783020002331
# 0.7875231560001339
# 0.799043344999518
