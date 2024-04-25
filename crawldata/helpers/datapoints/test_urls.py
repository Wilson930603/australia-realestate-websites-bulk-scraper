from crawldata.helpers.datapoints.base import BaseExtract


class TestListingsUrls(BaseExtract):
    def get_regex(self):
        for regex in [
            r'<h3[^>]+ itemprop="headline"> <a href="([^"]+)"[^>]+>',
            r'<div class="property\-address">\s*<a href="([^"]+)">',
            r'<a href="([^"]+)" aria\-label="View Listing Details">',
            r'<a[^>]+href="([^"]+)">More info',
            r'<a href="([^"]+)" +class="property\-card__link">',
            r'<div class="title"><a href="([^"]+)">',
            r'<div class="property_listing[^"]+"\s+data\-link="([^"]+)">',
            r'<a href="([^"]+\/property\/[^"]+)">',
            r'<a href="([^"]+\/property_listings\/[^"]+)">',
            r'<a href="([^"]+)"[^>]+class="listing\-url">',
            r'<a[^>]+href="([^"]+\/property\/[^"]+)">',
        ]:
            result = self.regex_match(regex, multi=True)
            if result:
                return regex, result

    def extract_urls(self):
        return self.get_regex()
