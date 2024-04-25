import os
import scrapy
from crawldata.helpers.utils import *
from crawldata.helpers.database import Database
from crawldata.helpers.sel import SeleniumSpider
from crawldata.helpers.datapoints.data import crawlDatapoints


class CrawlerSpider(scrapy.Spider):
    name = 'property'

    def start_requests(self):
        server = server_info()
        server_id = server['CurrentServer']
        db = Database()
        regex_list = db.load_data_regex()
        rows = db.load_property_temp(server_id)
        db.update_temp_property(server_id)
        for row in rows:
            url_found = row['url_found'].replace('\\/', '/')
            website = extract_domain(url_found)
            regex_site = regex_list.get(website, {})
            if row['type'] == 'selenium':
                yield scrapy.Request(url=url_found, callback=self.parse_selenium, meta={'row': row, 'regex': regex_site})
            else:
                yield scrapy.Request(url=url_found, callback=self.parse, meta={'row': row, 'regex': regex_site})

    def parse(self, response):
        base_url = extract_base(response.url)
        crawl_obj = crawlDatapoints(html_content=response.text, base_url=base_url, regex_list=response.meta['regex'])
        result = crawl_obj.crawl()
        row = response.meta['row']
        result['url'] = row['url_found']
        result['business_id'] = row['business_id']
        result['search_type'] = row['search_type']
        result['hash_url'] = hash_url(result['url'])

        hash_content = hash_json(result)
        result['hash_content'] = hash_content

        html_path = f'data/html/{hash_content}.html'
        result['html_path'] = html_path

        # images = result['images']

        if not os.path.exists(html_path):
            result['table'] = 'property'
            result = json_text(result)
            # with open(html_path, 'w', encoding='utf-8-sig') as file:
            #     file.write(response.text)
            yield result
        # if images:
        #     for image_url in images:
        #         hash_image_url = hash_url(image_url)
        #         yield {
        #             'table': 'property_images',
        #             'property_hash': hash_content,
        #             'hash_url': hash_image_url,
        #             'url': image_url,
        #             'path': f'data/images/{hash_image_url}.jpg'
        #         }
        #         if not os.path.exists(f'data/images/{hash_image_url}.jpg'):
        #             yield scrapy.Request(url=image_url, callback=self.save_image, meta={'hash_image_url': hash_image_url})

    def parse_selenium(self, response):
        base_url = extract_base(response.url)
        sel = SeleniumSpider()
        sel.get(response.url)
        sel.wait(10)
        source = sel.get_page_source()
        crawl_obj = crawlDatapoints(html_content=source, base_url=base_url, regex_list=response.meta['regex'])
        result = crawl_obj.crawl()

        row = response.meta['row']
        result['url'] = row['url_found']
        result['business_id'] = row['business_id']
        result['search_type'] = row['search_type']
        result['hash_url'] = hash_url(result['url'])

        hash_content = hash_json(result)
        result['hash_content'] = hash_content

        html_path = f'data/html/{hash_content}.html'
        result['html_path'] = html_path

        # images = result['images']

        if not os.path.exists(html_path):
            result['table'] = 'property'
            result = json_text(result)
            # with open(html_path, 'w', encoding='utf-8-sig') as file:
            #     file.write(response.text)
            yield result
    #     if images:
    #         for image_url in images:
    #             hash_image_url = hash_url(image_url)
    #             yield {
    #                 'table': 'property_images',
    #                 'property_hash': hash_content,
    #                 'hash_url': hash_image_url,
    #                 'url': image_url,
    #                 'path': f'data/images/{hash_image_url}.jpg'
    #             }
    #             if not os.path.exists(f'data/images/{hash_image_url}.jpg'):
    #                 yield scrapy.Request(url=image_url, callback=self.save_image, meta={'hash_image_url': hash_image_url})
    
    # def save_image(self, response):
    #     hash_image_url = response.meta['hash_image_url']
    #     with open(f'data/images/{hash_image_url}.jpg', 'wb') as file:
    #         file.write(response.body)
