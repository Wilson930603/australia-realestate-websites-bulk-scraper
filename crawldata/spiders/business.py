import scrapy
from crawldata.helpers.database import Database
from crawldata.helpers.sel import SeleniumSpider
from crawldata.helpers.datapoints.burls import BusinessUrls
from crawldata.helpers.utils import extract_base, server_info


class BusinessSpider(scrapy.Spider):
    name = 'business'
    handle_httpstatus_list = [403, 404, 500, 502, 503, 504]

    def start_requests(self):
        db = Database()
        regex_list = db.load_listing_regex()
        urls = db.get_unchecked_urls()
        server = server_info()
        server_id = server['CurrentServer']
        nb_servers = server['NumberOfServers']
        len_urls = len(urls)
        nb_urls_chunk = len_urls // nb_servers
        if server_id == nb_servers:
            urls = urls[(server_id-1)*nb_urls_chunk:]
        else:
            urls = urls[(server_id-1)*nb_urls_chunk:server_id*nb_urls_chunk]
        for url in urls:
            website = url['website']
            regex_site = regex_list.get(website, {})
            spider_type = url['type']
            if spider_type == 'selenium':
                yield scrapy.Request(
                    url=website,
                    meta={
                        'url': website,
                        'regex': regex_site,
                    },
                    callback=self.parse_selenium,
                )
            else:
                yield scrapy.Request(
                    url=website,
                    meta={
                        'url': website,
                        'regex': regex_site,
                    },
                    errback=self.parse_error
                )
    
    def parse_error(self, failure):
        yield {
            'table': 'business_listings_error',
            'url': failure.request.meta['url'],
            'note': f'{failure.value}'
        }
        yield {
            'table': 'count',
            'type': 'error'
        }

    def parse(self, response):
        status_code = response.status
        if status_code == 200:
            base_url = extract_base(response.url)
            crawl_obj = BusinessUrls(html_content=response.text, base_url=base_url, regex_list=response.meta['regex'])
            data = crawl_obj.extract()
            if data:
                yield {
                    'table': 'business_listings',
                    'url': response.meta['url'],
                    'data': data
                }
                yield {
                    'table': 'count',
                    'type': 'success'
                }
            else:
                yield {
                    'table': 'business_listings_error',
                    'url': response.meta['url'],
                    'note': 'No data found'
                }
                yield {
                    'table': 'count',
                    'type': 'success/no_data'
                }
        else:
            yield {
                'table': 'business_listings_error',
                'url': response.meta['url'],
                'note': f'HTTP {status_code}'
            }
            yield {
                'table': 'count',
                'type': 'error'
            }

    def parse_selenium(self, response):
        base_url = extract_base(response.url)
        sel = SeleniumSpider()
        sel.get(response.url)
        sel.wait(10)
        source = sel.get_page_source()
        crawl_obj = BusinessUrls(html_content=source, base_url=base_url, regex_list=response.meta['regex'])
        data = crawl_obj.extract()
        if data:
            yield {
                'table': 'business_listings',
                'url': response.meta['url'],
                'data': data
            }
            yield {
                'table': 'count',
                'type': 'success'
            }
        else:
            yield {
                'table': 'business_listings_error',
                'url': response.meta['url'],
                'note': 'No data found'
            }
            yield {
                'table': 'count',
                'type': 'success/no_data'
            }
