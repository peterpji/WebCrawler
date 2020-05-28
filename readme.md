
# WebCrawler
This is a simple web crawler which searches every href link from a webpage and if they are in the same domain adds them to the crawl queue. The final output is a file containing a list of pages on the domain.

This crawler could be easily expanded to e.g. log news headlines and the example site is a Finnish news site.

# Config
main.py has a few global variables which act as the config of the software.
- DOMAIN refers to the domain being crawled and it is also the first URL to be parsed.
- MAX_ITERATIONS refers to the maximum number of pages the crawlers processes before exiting if the crawling queue has not emptied
- TCP_CONNECTOR_LIMIT refers to the maximum number of connections the asyncio session allows
- Finally, file locations can be configured here

# Performance
The performance of the crawler is quite high due to quick parsing with lxml and asyncronous web requests. Small improvements could be made to CPU speed by switching completely from bs4 to lxml. However, the main bottleneck is internet speed so CPU usage optimization does not seem very productive.

# Dependencies
Python 3.8.1+
Additional libraries: aiohttp, bs4, lxml
