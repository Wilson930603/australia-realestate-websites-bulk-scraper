import scrapy
import pandas as pd
from crawldata.helpers.datapoints.test_urls import TestListingsUrls
from crawldata.helpers.utils import extract_domain, extra_points, extract_base


class TestSpider(scrapy.Spider):
    name = 'test'

    def start_requests(self):
        rows = pd.read_csv('daily.csv').to_dict('records')
        for row in rows:
            yield scrapy.Request(
                url=row['business_listing_url'],
                meta=row,
                dont_filter=True,
                callback=self.parse
            )
    
    def parse(self, response):
        meta = response.meta
        base_url = extract_base(response.url)
        crawl_obj = TestListingsUrls(html_content=response.text, base_url=base_url)
        regex, _ = crawl_obj.extract_urls()
        domain = extract_domain(response.url)
        points = extra_points(domain)
        note = ''
        if points.get('selenium'):
            note = 'selenium'
        elif regex:
            note = 'ok'
        if regex:
            yield {
                'id': meta['id'],
                'website': meta['website'],
                'business_listing_url': meta['business_listing_url'],
                'search_type': meta['search_type'],
                'regex': regex,
                'paging_system': '1' if points.get('pagination') else '0',
                'note': note,
            }
