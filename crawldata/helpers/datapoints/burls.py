from crawldata.helpers.utils import get_url
from crawldata.helpers.datapoints.base import BaseExtract


class BusinessUrls(BaseExtract):
    def is_forbidden(self, res):
        reject_list = ['javascript', 'Javascript']
        for reject in reject_list:
            if reject in res:
                return True
        starts_with = ['#', 'tel:', 'mailto:']
        for start in starts_with:
            if res.startswith(start):
                return True
        return False
    
    def extract_buy_listings_url(self):
        regex = self.regex_list.get('buy')
        if regex:
            result = self.regex_match(regex)
            if result:
                return result
        for regex in [
            r'<a[^>]+href="([^"]+)">Find Properties For Sale',
            r'<a href="([^"]+)"[^>]+>Residential Properties \- For Sale',
            r'<a[^>]+href="([^"]+)">Residential Sales',
            r'<a href="([^"]+)">Properties to Buy',
            r'<a href="([^"]+)">Property Search',
            r'<a[^>]+href="([^"]+)">\s*Search for properties',
            r'<a[^>]+href="([^"]{2,})"[^>]*>\s*Houses &amp; Properties For Sale',
            r'<a[^>]+href=\'([^\']{2,})\'[^>]*>\s*Houses &amp; Properties For Sale',
            r'<a[^>]+href="([^"]{2,}sale)"[^>]*>\s*Browse Properties',
            r'<a[^>]+href=\'([^\']{2,}sale)\'[^>]*>\s*Browse Properties',
            r'<a[^>]+href="([^"]{2,})"[^>]*>\s*Homes for sale',
            r'<a[^>]+href=\'([^\']{2,})\'[^>]*>\s*Homes for sale',
            r'<a[^>]+href="([^"]{2,})"[^>]*>\s*Properties For Sale',
            r'<a[^>]+href=\'([^\']{2,})\'[^>]*>\s*Properties For Sale',
            r'<a[^>]+href="([^"]{2,})"[^>]*>\s*Residential for Sale',
            r'<a[^>]+href=\'([^\']{2,})\'[^>]*>\s*Residential for Sale',
            r'<a[^>]*href="([^"]+)"[^>]*>\s*For Sale',
            r'<a[^>]*href="([^"]+)"[^>]*>Our Properties',
            r'<a[^>]+href="([^"]{2,})"[^>]*>\s*House &amp; Land',
            r'<a[^>]+href=\'([^\']{2,})\'[^>]*>\s*House &amp; Land',
            r'<a[^>]+href="([^"]{2,})"[^>]*>\s*<i class="[^"]+"><\/i><\w+>For Sale',
            r'<a[^>]+href=\'([^\']{2,})\'[^>]*>\s*<i class="[^"]+"><\/i><\w+>For Sale',
            r'<a class="[^"]+" href="([^"]+)">\s*<span class="[^"]+">\s*<span class="[^"]+">Buyers\/Tenants',
            r'<a[^>]+href="([^"]+)"[^>]+>(<div[^>]+>)+<p[^>]+>BUY OR SELL',
            r'<a href="([^"]+)"[^>]+><span[^>]+>Buying &#038; Selling',
            r'<a +href="([^"]+)"[^>]+><span>Residential',
            r'<a href="([^"]+)">Residential',
            r'<a class="nav-link" href="([^"]+)">For Sale',
            r'<a[^>]*href="([^"]+)"[^>]*>FOR SALE',
            r'<a href="([^"]+)" target="">Search All Properties',
            r'<a\s+href="([^"]+)"[^>]*>Home and Land Packages',
            r'<h4[^>]+>Featured Listings<\/h4>\s*<div[^>]+>\s*<a[^>]*href="([^"]+)"[^>]*>View All',
            r'"name":"Buying","url":"([^"]+)",',
            r'<a[^>]*href="([^^"]+)"><span>Real Estate Listings',
            r'<a[^>]*href="([^"]+)"[^>]*>Our Properties For Sale',
            r'<a[^>]*href="([^"]+)"[^>]*><span[^>]*>Listings',
            r'<a class="[^"]+" href="([^"]+)" >\s*Buy',
            r'<a[^>]+href="([^"]{2,})"[^>]*>\s*Buy',
            r'<a[^>]+href=\'([^\']{2,})\'[^>]*>\s*Buy',
            r'<a href="([^"]+)">Buy',
            r'<a\s+href="([^"]+)"[^>]*>\s*Buy',
            r'<a[^>]*href="([^"]+)"[^>]*><span[^>]*>Buy',
            r'<a[^>]*href="([^"]+)"[^>]*>\s*My Listings',
        ]:
            results = self.regex_match(regex, multi=True)
            if results:
                for result in results:
                    if not self.is_forbidden(result):
                        return result

    def extract_rent_listings_url(self):
        regex = self.regex_list.get('rent')
        if regex:
            result = self.regex_match(regex)
            if result:
                return result
        for regex in [
            r'<a[^>]+href="([^"]{2,})"[^>]*>\s*Houses &amp; Properties For Lease',
            r'<a[^>]+href=\'([^\']{2,})\'[^>]*>\s*Houses &amp; Properties For Lease',
            r'<a[^>]+href="([^"]{2,}lease)"[^>]*>\s*Residential',
            r'<a[^>]+href=\'([^\']{2,}lease)\'[^>]*>\s*Residential',
            r'<a[^>]+href="(\/rent\/[^"]{2,})"[^>]*>\s*Available Properties',
            r'<a[^>]+href=\'(\/rent\/[^\']{2,})\'[^>]*>\s*Available Properties',
            r'<a[^>]+href="([^"]{2,})"[^>]*>\s*Properties For Rent',
            r'<a[^>]+href=\'([^\']{2,})\'[^>]*>\s*Properties For Rent',
            r'<a[^>]+href="([^"]{2,})"[^>]*>\s*Residential For Rent',
            r'<a[^>]+href=\'([^\']{2,})\'[^>]*>\s*Residential For Rent',
            r'<a[^>]+href="([^"]{2,})"[^>]*>\s*<i class="[^"]+"><\/i><\w+>Rental Search',
            r'<a[^>]+href=\'([^\']{2,})\'[^>]*>\s*<i class="[^"]+"><\/i><\w+>Rental Search',
            r'<a[^>]+href="([^"]{2,})"[^>]*>\s*For Lease',
            r'<a[^>]+href=\'([^\']{2,})\'[^>]*>\s*For Lease',
            r'<a[^>]+href="([^"]{2,})"[^>]*>\s*Leasing',
            r'<a[^>]+href=\'([^\']{2,})\'[^>]*>\s*Leasing',
            r'<a[^>]+href="([^"]{2,})"[^>]*>\s<\w+>*Bookings \+ Contact',
            r'<a[^>]+href=\'([^\']{2,})\'[^>]*>\s<\w+>*Bookings \+ Contact',        
            r'<a[^>]+href="([^"]{2,})"[^>]*>\s*Rent',
            r'<a[^>]+href=\'([^\']{2,})\'[^>]*>\s*Rent',            
            r'<a class="[^"]+" href="([^"]+)">\s*<span class="[^"]+">\s*<span class="[^"]+">Buyers\/Tenants',
            r'<a href="([^"]+)"[^>]+><span[^>]+>Vacation Rental Management',
            r'<a href="([^"]+)">Leasing',
            r'<a class="nav-link" href="([^"]+)">For Rent',
            r'<a[^>]*href="([^"]+)"[^>]*>(\s*<span[^>]*>)*BOOK NOW',
            r'<a href="([^"]+)">Rent',
            r'<a[^>]*href="([^"]+)"[^>]*><span[^>]*>Rent',
            r'<a class="[^"]+" href="([^"]+)" >\s*Lease',
            r'<a\s+href="([^"]+)"[^>]*><span>Available Rentals',
            r'<a[^>]*href="([^"]+)">Rental Properties',
            r'<a[^>]*href="([^"]+)"[^>]*>For Rent Listings',
            r'<a[^>]*href="([^"]+)"[^>]*>Book',
            r'<a[^>]*href="([^"]+)"[^>]*>For Rent',
            r'<a[^>]*href="([^"]+)"[^>]*>\s*For Rent',
        ]:
            results = self.regex_match(regex, multi=True)
            if results:
                for result in results:
                    if not self.is_forbidden(result):
                        return result

    def extract_sold_listings_url(self):
        regex = self.regex_list.get('sold')
        if regex:
            result = self.regex_match(regex)
            if result:
                return result
        for regex in [
            r'<a[^>]+href="([^"]{2,})"[^>]*>\s*Sold Properties',
            r'<a[^>]+href=\'([^\']{2,})\'[^>]*>\s*Sold Properties',
            r'<a[^>]+href="([^"]{2,})"[^>]*>\s*Recent Sales',
            r'<a[^>]+href=\'([^\']{2,})\'[^>]*>\s*Recent Sales',
            r'<a[^>]*href="([^"]+)"[^>]*>Recent Sales',
            r'<a[^>]+href="([^"]{2,})"[^>]*>\s*Recently Sold',
            r'<a[^>]+href=\'([^\']{2,})\'[^>]*>\s*Recently Sold',
            r'<a class="[^"]+" href="([^"]+)" >\s*Our Sold Properties',
            r'<a[^>]*href="([^"]+)"[^>]*>Sales',
            r'<a\s+href="([^"]+)"[^>]*>\s*Sold',
            r'<a href="([^"]+)">Sold',
            r'<a[^>]*href="([^"]+)"[^>]*>Sold Properties',
            r'<a[^>]*href="([^"]+)"[^>]*>PREVIOUSLY SOLD',
        ]:
            results = self.regex_match(regex, multi=True)
            if results:
                for result in results:
                    if not self.is_forbidden(result):
                        return result

    def extract(self):
        buy = self.extract_buy_listings_url()
        rent = self.extract_rent_listings_url()
        sold = self.extract_sold_listings_url()
        buy = get_url(self.base_url, buy)
        rent = get_url(self.base_url, rent)
        sold = get_url(self.base_url, sold)
        if not buy and not rent and not sold:
            return None
        return {
            'buy_listings_url': buy,
            'rent_listings_url': rent,
            'sold_listings_url': sold,
        }
