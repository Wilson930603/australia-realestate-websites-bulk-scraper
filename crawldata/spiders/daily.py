import scrapy
from crawldata.helpers.database import Database


class DailySpider(scrapy.Spider):
    name = 'daily'
    handle_httpstatus_list = [403, 404, 500, 502, 503, 504]
    
    def start_requests(self):
        db = Database()
        listings = db.load_daily_listing()
        for listing in listings:
            yield scrapy.Request(
                url=listing['website'],
                meta=listing,
                dont_filter=True,
                callback=self.parse
            )
    
    def parse(self, response):
        meta = response.meta
        business_id = meta['id']
        if meta['buy_listings_url']:
            yield {
                'id': business_id,
                'website': meta['website'],
                'business_listing_url': meta['buy_listings_url'],
                'search_type': 'BUY',
            }
        if meta['rent_listings_url']:
            yield {
                'id': business_id,
                'website': meta['website'],
                'business_listing_url': meta['rent_listings_url'],
                'search_type': 'RENT',
            }
        if meta['sold_listings_url']:
            yield {
                'id': business_id,
                'website': meta['website'],
                'business_listing_url': meta['sold_listings_url'],
                'search_type': 'SOLD',
                'regex': '',
                'paging_system': '',
                'note': '',
            }
