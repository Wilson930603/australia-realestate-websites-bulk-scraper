import os
import scrapy
from crawldata.helpers.sel import SeleniumSpider
from crawldata.helpers.utils import extract_base
from crawldata.helpers.datapoints.paging import PagingUrl
from crawldata.helpers.datapoints.urls import ListingsUrls
from crawldata.helpers.datapoints.burls import BusinessUrls
from crawldata.helpers.datapoints.data import crawlDatapoints


class RipeSpider(scrapy.Spider):
    name = 'ripe'

    if os.path.exists('ripe.csv'):
        os.remove('ripe.csv')
    custom_settings = {
        "FEEDS": {
            "ripe.csv": {
                "format": "csv",
                "item_export_kwargs": {
                    "include_headers_line": True
                }
            }
        }
    }

    def __init__(self, website_url=None, business_listing_url=None, selenium=None, property_url=None, **kwargs):
        self.website_url = website_url
        self.business_listing_url = business_listing_url
        self.selenium = selenium
        self.property_url = property_url
    
    def start_requests(self, *args, **kwargs):
        if self.website_url:
            if self.selenium:
                yield scrapy.Request(
                    url=self.website_url,
                    callback=self.parse_business_selenium,
                )
            else:
                yield scrapy.Request(
                    url=self.website_url,
                    callback=self.parse_business,
                )
        elif self.business_listing_url:
            if self.selenium:
                yield scrapy.Request(url=self.business_listing_url, callback=self.parse_listing_selenium)
            else:
                yield scrapy.Request(
                    url=self.business_listing_url,
                    callback=self.parse_listing,
                    meta={'urls': []}
                )
        elif self.property_url:
            if self.selenium:
                yield scrapy.Request(
                    url=self.property_url,
                    callback=self.parse_property_selenium,
                )
            else:
                yield scrapy.Request(
                    url=self.property_url,
                    callback=self.parse_property,
                )

    def parse_business(self, response):
        base_url = extract_base(response.url)
        obj = BusinessUrls(response.text, base_url)
        urls = obj.extract()
        if not urls:
            yield {
                'url': response.url,
                'status': 'No urls found',
            }
        else:
            yield {
                'url': response.url,
                **urls
            }

    def parse_business_selenium(self, response):
        base_url = extract_base(response.url)
        sel = SeleniumSpider()
        sel.get(response.url)
        sel.wait(10)
        source = sel.get_page_source()
        crawl_obj = BusinessUrls(html_content=source, base_url=base_url, regex_list={})
        urls = crawl_obj.extract()
        if not urls:
            yield {
                'url': response.url,
                'status': 'No urls found',
            }
        else:
            yield {
                'url': response.url,
                **urls
            }

    def parse_listing(self, response):
        base_url = extract_base(response.url)
        obj = ListingsUrls(response.text, base_url, {})
        urls = obj.extract_urls()
        if not urls and not response.meta['urls']:
            yield {
                'url': response.url,
                'status': 'No urls found',
            }
        elif urls:
            urls = list(set(urls) - set(response.meta['urls']))
            if urls:
                for url in urls:
                    yield {
                        'url': response.url,
                        'property_url': url,
                    }
                obj_page = PagingUrl(response.text, base_url, {})
                next_page = obj_page.extract_next_page()
                if next_page:
                    urls.extend(response.meta['urls'])
                    yield scrapy.Request(
                        url=next_page,
                        callback=self.parse_listing,
                        meta={'urls': urls},
                        dont_filter=True
                    )

    def parse_listing_selenium(self, response):
        base_url = extract_base(response.url)
        sel = SeleniumSpider()
        sel.get(response.url)
        sel.wait(10)
        source = sel.get_page_source()
        crawl_obj = ListingsUrls(html_content=source, base_url=base_url, regex_list={})
        urls = crawl_obj.extract_urls()
        if not urls:
            yield {
                'url': response.url,
                'status': 'No urls found',
            }
        else:
            for url in urls:
                yield {
                    'url': response.url,
                    'property_url': url,
                }

    def parse_property(self, response):
        base_url = extract_base(response.url)
        obj = crawlDatapoints(response.text, base_url, {})
        data = obj.crawl()
        if not data:
            yield {
                'url': response.url,
                'status': 'No data found',
            }
        else:
            yield {
                'url': response.url,
                **data
            }

    def parse_property_selenium(self, response):
        base_url = extract_base(response.url)
        sel = SeleniumSpider()
        sel.get(response.url)
        sel.wait(10)
        source = sel.get_page_source()
        crawl_obj = crawlDatapoints(html_content=source, base_url=base_url, regex_list={})
        data = crawl_obj.crawl()
        if not data:
            yield {
                'url': response.url,
                'status': 'No data found',
            }
        else:
            yield {
                'url': response.url,
                **data
            }
