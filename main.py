import logging
import os
import time
import asyncio
import aiohttp
from spider import Spider

logging.getLogger().setLevel(15)

DOMAIN = 'http://www.hs.fi/'
MAX_BATCHES = 100
TCP_CONNECTOR_LIMIT = 1_000
CRAWL_BATCH_SIZE = 100

current_dir = os.path.dirname(os.path.realpath(__file__))
QUEUE_FILE = os.path.join(current_dir, 'output', 'queue.txt')
CRAWLED_FILE = os.path.join(current_dir, 'output', 'crawled.txt')


async def main():
    logging.info('Crawling max %s pages', MAX_BATCHES * CRAWL_BATCH_SIZE)

    connector = aiohttp.TCPConnector(limit=TCP_CONNECTOR_LIMIT)

    async with aiohttp.ClientSession(connector=connector) as session:
        spider = Spider(session, QUEUE_FILE, CRAWLED_FILE, DOMAIN)
        for _ in range(MAX_BATCHES):
            await spider.crawl_batch(CRAWL_BATCH_SIZE)

    # In the current aiohttp version, there is a bug in _ProactorBasePipeTransport.__del__
    # In the bug, async with won't wait for session to close properly throwing a harmless but annoying exception when exiting.
    await asyncio.sleep(0.2)


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    logging.info('Time taken: %s', time.time() - start)
