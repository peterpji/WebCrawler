import logging
from urllib.parse import urlparse
import asyncio
from aiohttp.client_exceptions import ClientConnectorError

from general_functions import import_file_to_set, export_set_to_file, create_file
from html_link_parser import Html_link_parser


class Spider:
    def __init__(self, session, queue_file, crawled_file, domain):
        self.count_crawled = 0
        self.session = session
        self.queue_file = queue_file
        self.crawled_file = crawled_file
        self.domain = self._normalize_domain(domain)

        create_file(queue_file)
        create_file(crawled_file)
        self.queue = import_file_to_set(queue_file)
        self.crawled = import_file_to_set(crawled_file)

        if domain not in self.crawled:
            logging.info('Inserting domain %s to queue', domain)
            self.queue.add(domain)
        else:
            logging.warning('Domain %s is already crawled', domain)

    async def crawl_next_from_queue(self):
        if not self.queue:
            return

        link = self.queue.pop()
        assert self._normalize_domain(link) == self.domain

        page_content = await self._get_page(link)

        found_links = self._parse_page_hrefs(page_content, link)

        self._update_crawled_queue_sets(found_links, link)

    async def crawl_batch(self, batch_size):
        if not self.queue:
            return

        tasks = []
        for _ in range(batch_size):
            if self.queue:
                tasks.append(self.crawl_next_from_queue())
            else:
                logging.info('Queue empty. Finishing batch')
                break
        await asyncio.gather(*tasks)
        self.save_results()
        self.status_report()

    def status_report(self):
        logging.info('Spider queue: %s', len(self.queue))
        logging.info('Spider crawled: %s', len(self.crawled))

    def save_results(self):
        self._update_files()

    async def _get_page(self, page_url):
        logging.debug('Page url: %s', page_url)

        try:
            response = await self.session.get(page_url)

        except ClientConnectorError:
            logging.debug('No response from %s', page_url)
            return ''

        logging.debug(response.status)
        response = await response.text(encoding='utf-8')

        return response

    def _parse_page_hrefs(self, content, source_url):
        parser = Html_link_parser(content, source_url)
        return parser.constructed_urls

    def _update_crawled_queue_sets(self, links, source_page_url):
        for link in links:
            if link not in self.crawled and self._normalize_domain(link) == self.domain:
                self.queue.add(link)

        self.crawled.add(source_page_url)

    def _update_files(self):
        export_set_to_file(self.queue, self.queue_file)
        export_set_to_file(self.crawled, self.crawled_file)

    def _normalize_domain(self, page_url):
        return urlparse(page_url).netloc
