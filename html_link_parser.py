import logging
from bs4 import BeautifulSoup, SoupStrainer
import lxml.html


class Html_link_parser(object):

    def __init__(self, html_page, source_url):
        self.raw_href_list = self._html_parser(html_page)
        self.constructed_urls = self._construct_urls(self.raw_href_list, source_url)


    def _html_parser(self, html_page):
        tree = lxml.html.document_fromstring(html_page.encode())

        raw_href_list = []
        for link in tree.xpath('.//a'):
            href = link.get('href')
            if href:
                raw_href_list.append(href)

        return raw_href_list


    def _construct_urls(self, raw_href_list, source_url):

        constructed_urls = []
        for link in raw_href_list:
            if '#' in link:
                link = link.split('#')[0]
            if not link:
                continue

            if '.' not in link.replace('//','').split('/')[0]:
                if '/' != link[0]:
                    constructed_urls.append('/'.join(source_url.split('/')[:-1] + [link]))
                else:
                    constructed_urls.append('/'.join(source_url.split('/')[:3] + [link[1:]]))
            else:
                if ':' in link:
                    if link.split(':')[0] in ['http', 'https']:
                        constructed_urls.append(link)
                    else:
                        logging.debug('Not a web url schema')
                else:
                    constructed_urls.append('http://' + link)

        for index in range(0, len(constructed_urls)):
            if constructed_urls[index][-1] != '/':
                constructed_urls[index] = constructed_urls[index] + '/'

        constructed_urls = [link for link in constructed_urls if link and link != source_url]

        return constructed_urls


    def _construct_urls_v2(self, raw_href_list, source_url): # TODO: FINISH
        import re

        def split_url(link):
            schema = re.match(r'^[a-zA-Z0-9]+:[//]', link)
            if schema:
                schema = schema.group()
                link = link[len(schema):]
            else:
                schema = ''

            if '.' in str(link + '/').split('/')[0]:
                netloc = re.match(r'^[a-zA-Z0-9-_.]+', link)
                if netloc:
                    link = link[len(netloc):]
                else:
                    netloc = ''

                port = re.match(r'^:[0-9]+', link)
                if port:
                    link = link[len(port):]
                else:
                    port = ''

                path = link
                if path and '#' in path:
                    path = path.split('#')[0]
            else:
                path = link
                schema = ''
                netloc = ''
                port = ''

            if schema or netloc or port or path:
                link = {'schema': schema, 'netloc': netloc, 'port': port, 'path': path}
                return link
            else:
                return None

        def merge_urls(source_url, raw_href_list):
            source_url = split_url(source_url)
            constructed_urls = []
            for link in raw_href_list:
                link = split_url(link)

                if not link:
                    continue

                constructed_url = ''
                for part in ['schema', 'netloc', 'port']:
                    if link[part]:
                        constructed_url = constructed_url + link[part]
                    else:
                        constructed_url = constructed_url + source_url[part]

                if link['path'] and link['path'][0] == '/':
                    constructed_url = constructed_url + link['path']
                elif link['path']:
                    if source_url['path']:
                        base_path = '/'.join(source_url['path'].split('/')[:-1]) + '/'
                    else:
                        base_path = '/'
                    constructed_url = constructed_url + base_path + link['path']

                constructed_urls.append(constructed_url)

            return constructed_urls

        constructed_urls = merge_urls(source_url, raw_href_list)
        for index in range(0, len(constructed_urls)):
            if constructed_urls[index][-1] != '/':
                constructed_urls[index] = constructed_urls[index] + '/'

        constructed_urls = [link for link in constructed_urls if link != source_url]

        return constructed_urls


if __name__ == "__main__":
    source_url = 'http://hs.fi/kotimaa/art-2000006331170.html/'
    html = "<html><head class='jee'><title>Test</title></head><body><h1>Parse me! <a class='link' href='www.google.com' aProp='jee2'>Here is Google</a><a class='link' href='/home' aProp='jee2'>And here is home</a><a></a><a href=http://google.com></a><a href=https://google.com></a><a href=https://google.com/images></a><a href=acdc></a></h1></body><a href=#page-main-content></a></html>"
    parser = Html_link_parser(html, source_url)
    print(f'Source: {source_url}; Raw: {parser.raw_href_list}; Constructed: {parser.constructed_urls}')
