import logging
import os
import time
import asyncio
import aiohttp
from spider import Spider

logging.getLogger().setLevel(15)

DOMAIN = "http://www.hs.fi/"
QUEUE_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output', "queue.txt")
CRAWLED_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output', "crawled.txt")
MAX_ITERATIONS = 1000000
TCP_CONNECTOR_LIMIT = 1_000


async def main():

    async def loop_through_links(spider):
        for iterations in range(MAX_ITERATIONS):
            if iterations % 100 == 0:
                logging.info('Starting iteration %s', iterations)
                spider.status_report()

            if spider.queue:
                await spider.crawl_next_from_queue()
            else:
                logging.info('Queue empty. Closing')
                break

    connector = aiohttp.TCPConnector(limit=TCP_CONNECTOR_LIMIT)
    spider = Spider(connector, QUEUE_FILE, CRAWLED_FILE, DOMAIN)
    await loop_through_links(spider)


if __name__ == "__main__":
    start = time.time()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    # asyncio.run(main())

    logging.info('Time taken: %s', time.time()-start)
