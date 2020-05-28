import logging
import os
import time
import asyncio
import aiohttp
from spider import Spider

logging.getLogger().setLevel(15)

DOMAIN = "http://www.hs.fi/"
MAX_ITERATIONS = 10_000
TCP_CONNECTOR_LIMIT = 1_000

current_dir = os.path.dirname(os.path.realpath(__file__))
QUEUE_FILE = os.path.join(current_dir, 'output', "queue.txt")
CRAWLED_FILE = os.path.join(current_dir, 'output', "crawled.txt")


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
