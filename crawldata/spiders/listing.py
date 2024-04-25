import scrapy
from crawldata.helpers.utils import *
from crawldata.helpers.database import Database
from crawldata.helpers.sel import SeleniumSpider
from crawldata.helpers.datapoints.paging import PagingUrl
from crawldata.helpers.datapoints.urls import ListingsUrls


class ListingSpider(scrapy.Spider):
    name = 'listing'
    business_listings = []

    def start_requests(self):
        server = server_info()
        self.server_id = server['CurrentServer']
        nb_servers = server['NumberOfServers']
        db = Database()
        regex_list = db.load_property_regex()
        search = db.load_search_keys()
        len_search = len(search)
        nb_search_chunk = len_search // nb_servers
        if self.server_id == nb_servers:
            search = search[(self.server_id-1)*nb_search_chunk:]
        else:
            search = search[(self.server_id-1)*nb_search_chunk:self.server_id*nb_search_chunk]
        final_search = []
        for s in search:
            buy_listings_url = None
            rent_listings_url = None
            sold_listings_url = None
            if s['search_type'] == 'BUY':
                buy_listings_url = clean_url(s['site_path'])
            elif s['search_type'] == 'RENT':
                rent_listings_url = clean_url(s['site_path'])
            elif s['search_type'] == 'SOLD':
                sold_listings_url = clean_url(s['site_path'])
            final_search.append({
                'id': 'N/A',
                'type': s['type'],
                'pagination_xpath': s['pagination_xpath'],
                'buy_listings_url': buy_listings_url,
                'rent_listings_url': rent_listings_url,
                'sold_listings_url': sold_listings_url,
                'domain': extract_domain(s['website']),
                'listing_url': s['listing_url'],
            })
        db.purge_temp_property(self.server_id)
        listings = db.load_listings()
        listings = clean_duplicates(listings)
        len_listings = len(listings)
        nb_urls_chunk = len_listings // nb_servers
        if self.server_id == nb_servers:
            listings = listings[(self.server_id-1)*nb_urls_chunk:]
        else:
            listings = listings[(self.server_id-1)*nb_urls_chunk:self.server_id*nb_urls_chunk]
        listings = listings + final_search
        sites_to_run = sites_run()
        for listing in listings:
            if listing['buy_listings_url']:
                url = clean_url(listing['buy_listings_url'])
                domain = extract_domain(url)
                if sites_to_run and domain not in sites_to_run:
                    continue
                regex_site = regex_list.get(domain, {})
                yield scrapy.Request(
                    url=url,
                    meta={
                        'id': listing['id'],
                        'search_type': 'BUY',
                        'url': listing['buy_listings_url'],
                        'type': listing['type'],
                        'domain': domain,
                        'pagination_xpath': listing['pagination_xpath'],
                        'found': 0,
                        'urls': [],
                        'listing_url': listing.get('listing_url', None),
                        'regex': regex_site
                    },
                    dont_filter=True,
                    callback=self.parse if listing['type'] != 'selenium' else self.parse_selenium
                )
            # if listing['rent_listings_url']:
            #     url = clean_url(listing['rent_listings_url'])
            #     domain = extract_domain(url)
            #     yield scrapy.Request(
            #         url=url,
            #         meta={
            #             'id': listing['id'],
            #             'search_type': 'RENT',
            #             'url': listing['rent_listings_url'],
            #             'type': listing['type'],
            #             'domain': domain,
            #             'pagination_xpath': listing['pagination_xpath'],
            #             'found': 0,
            #             'urls': [],
            #             'listing_url': listing.get('listing_url', None)
            #         },
            #         dont_filter=True,
            #         callback=self.parse if listing['type'] != 'selenium' else self.parse_selenium
            #     )
            # if listing['sold_listings_url']:
            #     url = clean_url(listing['sold_listings_url'])
            #     domain = extract_domain(url)
            #     yield scrapy.Request(
            #         url=url,
            #         meta={
            #             'id': listing['id'],
            #             'search_type': 'SOLD',
            #             'url': listing['sold_listings_url'],
            #             'type': listing['type'],
            #             'domain': domain,
            #             'pagination_xpath': listing['pagination_xpath'],
            #             'found': 0,
            #             'urls': [],
            #             'listing_url': listing.get('listing_url', None)
            #         },
            #         dont_filter=True,
            #         callback=self.parse if listing['type'] != 'selenium' else self.parse_selenium
            #     )

    def parse(self, response):
        if response.meta['found'] == 0:
            yield {
                'table': 'count',
                'type': response.meta['search_type']
            }
        base_url = extract_base(response.url)
        crawl_obj = ListingsUrls(html_content=response.text, base_url=base_url, regex_list=response.meta['regex'])
        urls = crawl_obj.extract_urls()
        if urls or response.meta['found'] > 0:
            b_id = response.meta['id']
            if b_id not in self.business_listings:
                yield {
                    'table': 'business_with_listings_urls',
                    'business_id': b_id,
                    'note': 'ok'
                }
                self.business_listings.append(b_id)
            urls = list(set(urls) - set(response.meta['urls']))
            new_count = len(urls)
            next_page = None
            if new_count > 0:
                yield {
                    'table': 'count',
                    'type': 'total_links',
                    'count': new_count
                }
                response.meta['urls'].extend(urls)
                rows = []
                for url in urls:
                    rows.append({
                        'business_id': b_id,
                        'search_type': response.meta['search_type'],
                        'url_found': url,
                        'server_id': self.server_id
                    })
                yield {
                    'table': 'property_listing_urls_temp',
                    'rows': rows,
                }
                response.meta['found'] += new_count
                next_obj = PagingUrl(html_content=response.text, base_url=base_url, regex_list=response.meta['regex'])
                next_page = next_obj.extract_next_page()
            if next_page:
                yield scrapy.Request(
                    url=clean_url(next_page),
                    meta=response.meta,
                    dont_filter=True
                )
            else:
                yield {
                    'table': 'listing_stats',
                    'business_id': b_id,
                    'search_type': response.meta['search_type'],
                    'url': response.meta['listing_url'] if response.meta['listing_url'] else response.meta['url'],
                    'domain': response.meta['domain'],
                    'properties_found': response.meta['found']
                }
                yield {
                    'table': 'count',
                    'type': 'with_data'
                }
        else:
            yield {
                'table': 'count',
                'type': 'no_data'
            }

    def parse_selenium(self, response):
        yield {
            'table': 'count',
            'type': response.meta['search_type']
        }
        base_url = extract_base(response.url)
        sel = SeleniumSpider()
        sel.get(response.url)
        urls = []
        sel.wait(10)
        source = sel.get_page_source()
        crawl_obj = ListingsUrls(html_content=source, base_url=base_url, regex_list=response.meta['regex'])
        urls = crawl_obj.extract_urls()
        if urls:
            pagination_xpath = response.meta['pagination_xpath']
            if pagination_xpath:
                has_next = True
                has_next = False
                while has_next:
                    el = sel.locate_element(pagination_xpath)
                    print("My element is: ", el)
                    if not el:
                        break
                    sel.click_element(el)
                    sel.wait(5)
                    source = sel.get_page_source()
                    crawl_obj = ListingsUrls(html_content=source, base_url=base_url, regex_list=response.meta['regex'])
                    page_urls = crawl_obj.extract_urls()
                    page_urls = list(set(page_urls) - set(urls))
                    if page_urls:
                        urls.extend(page_urls)
                    else:
                        break
            b_id = response.meta['id']
            if b_id not in self.business_listings:
                yield {
                    'table': 'business_with_listings_urls',
                    'business_id': b_id,
                    'note': 'ok'
                }
                self.business_listings.append(b_id)
            yield {
                'table': 'count',
                'type': 'total_links',
                'count': len(urls)
            }
            rows = []
            for url in urls:
                rows.append({
                    'business_id': b_id,
                    'search_type': response.meta['search_type'],
                    'url_found': url,
                    'server_id': self.server_id
                })
            yield {
                'table': 'property_listing_urls_temp',
                'rows': rows,
            }
            yield {
                'table': 'listing_stats',
                'business_id': b_id,
                'search_type': response.meta['search_type'],
                'url': response.meta['listing_url'] if response.meta['listing_url'] else response.meta['url'],
                'domain': response.meta['domain'],
                'properties_found': response.meta['found']
            }
        sel.quit()
