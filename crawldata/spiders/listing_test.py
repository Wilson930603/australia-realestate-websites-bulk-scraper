import scrapy
import pandas as pd
from crawldata.helpers.utils import extract_domain, extract_base
from crawldata.helpers.datapoints.test_urls import TestListingsUrls


class ListingTestSpider(scrapy.Spider):
    name = 'listing_test'

    def start_requests(self):
        data = pd.read_csv('test.csv')
        for row in data.to_dict('records'):
            if row['note'] == 'ok':
                yield scrapy.Request(
                    url=row['business_listing_url'],
                    meta=row,
                    dont_filter=True,
                    callback=self.parse
                )

    def parse(self, response):
        base_url = extract_base(response.url)
        crawl_obj = TestListingsUrls(html_content=response.text, base_url=base_url)
        _, urls = crawl_obj.extract_urls()
        domain = extract_domain(response.url)
        yield {
            'table': 'listing_stats_temp',
            'business_id': response.meta['id'],
            'search_type': response.meta['search_type'],
            'url': response.meta['business_listing_url'],
            'domain': domain,
            'properties_found': len(urls)
        }
