import os
from datetime import datetime
from crawldata.helpers.database import Database
from crawldata.helpers.utils import saving_log, server_info, final_log


class CrawldataPipeline:
    def open_spider(self, spider):
        self.db = Database()
        self.server_id = server_info()['CurrentServer']
        self.server_ip = server_info()['ServerIP']
        os.makedirs('logs', exist_ok=True)
        if spider.name == 'property':
            os.makedirs('data', exist_ok=True)
            os.makedirs('data/html', exist_ok=True)
            os.makedirs('data/images', exist_ok=True)
            os.makedirs('logs/property', exist_ok=True)
            self.count = {
                'start_time': str(datetime.now()),
                'total': 0,
                'end_time': ''
            }
        elif spider.name == 'business':
            os.makedirs('logs/business', exist_ok=True)
            self.count = {
                'start_time': str(datetime.now()),
                'total': 0,
                'success': 0,
                'success/no_data': 0,
                'error': 0,
                'end_time': ''
            }
        elif spider.name == 'listing':
            os.makedirs('logs/listing', exist_ok=True)
            self.count = {
                'start_time': str(datetime.now()),
                'BUY': 0,
                'RENT': 0,
                'SOLD': 0,
                'with_data': 0,
                'no_data': 0,
                'total_links': 0,
                'end_time': ''
            }

    def process_item(self, item, spider):
        if spider.name == 'listing':
            table = item['table']
            del item['table']
            if table == 'property_listing_urls_temp':
                self.db.insert_temp_property(item['rows'])
            elif table == 'listing_stats':
                self.db.insert_listing_stats(item)
            elif table == 'business_with_listings_urls':
                self.db.update_business_with_listing(
                    item['business_id'],
                    item['note']
                )
            elif table == 'count':
                count_type = item['type']
                if count_type == 'total_links':
                    self.count['total_links'] += item['count']
                else:
                    self.count[count_type] += 1
        elif spider.name == 'property':
            table = item['table']
            del item['table']
            if table == 'property':
                self.db.insert_property(item)
                self.count['total'] += 1
            elif table == 'property_images':
                self.db.insert_property_images(item)
        elif spider.name == 'business':
            table = item['table']
            del item['table']
            if table == 'business_listings':
                self.db.update_url_checked(item['url'], item['data'])
            elif table == 'business_listings_error':
                self.db.update_url_checked_error(item['url'], item['note'])
            elif table == 'count':
                count_type = item['type']
                self.count[count_type] += 1
                self.count['total'] += 1
        elif spider.name == 'listing_test':
            table = item['table']
            del item['table']
            if table == 'listing_stats_temp':
                self.db.insert_listing_stats_temp(item)
        return item

    def close_spider(self, spider):
        spider_name = spider.name
        if spider_name in ['business', 'listing', 'property']:
            self.count['end_time'] = str(datetime.now())
            saving_log(self.count, spider_name)
        if spider_name == 'property':
            self.db.purge_temp_property(self.server_id)
            log = final_log(self.server_ip)
            self.db.insert_daily_cron_stats(log)
