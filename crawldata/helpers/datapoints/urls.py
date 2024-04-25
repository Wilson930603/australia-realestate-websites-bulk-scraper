from crawldata.helpers.utils import get_url
from crawldata.helpers.datapoints.base import BaseExtract


class ListingsUrls(BaseExtract):
    def get_urls(self):
        regex = self.regex_list.get('property')
        if regex:
            result = self.regex_match(regex, multi=True)
            if result:
                return result
        for regex in [
            r'<a href="([^"]+)"[^>]+title="More details"[^>]+>',
            r'<a href="([^"]+)" +class="property\-[^"]+">',
            r'<a href="(\/property[^"]+)" class="card">',
            r'<a class="propertyType" href="(\/property[^"]+)">',
            r'<a href="(\/property[^"]+)" rel="tag">',
            r'<a href="([^"]+\/property[^"]+)">',
            r'<a href="(\/property[^"]+)">',
            r'<a target="_blank" href="(\/property[^"]+)">',
            r'<h5 class="listing\-address"><a href="(\/real\-estate\/property\/[^"]+)" title="[^"]+">',
            r'<a class="centerimage" href="([^"]+)" title="[^"]+">',
            r'<a href="([^"]+)" class="listing\-featured\-[^"]+">',
            r'<a target=_self href="([^"]+\/property\/[^"]+)" class="listing\-featured\-thumb[^"]+">',
            r'<h2 class="h5"><a href="([^"]+\/property\-[^"]+)" target="_blank">',
            r'<a href="([^"]+\/homedetails\/[^"]+)"[^>]+>',
            r'<article class="[^"]+propertyListItemWrapper[^"]+"[^>]+>\s*<a href="([^"]+)">',
            r'<div[^>]+id="listing[^"]+">(?:\s*<div[^>]*>)+\s*<a[^>]+href="([^"]+)"[^>]+>',
            r'<a class="property\-link" href="([^"]+)"[^>]+>',
            r'<a[^>]+href="([^"]+\/listings\/[^"]+)"><div class="listing-card"',
            r'<div class="listing[^"]+">\s*<div[^>]*>\s*<figure[^>]+>\s*<a href="([^"]+)"[^>]*>',
            r'"id":\d+,"name":"[^"]+","slug":"[^"]+","excerpt":"[^"]+","link":"([^"]+)"',
            r'"Lat":"[^"]+","Long":"[^"]+","id":"[^"]+","url":"([^"]+)"',
            r'<div class="property\-address">\s*<a href="([^"]+)">',
            r'<div class="property\-overlay">\s*<a href="([^"]+)"[^>]+>',
            r'<div data\-ux="ContentCardWrapperImage"[^>]+><a data\-ux="Element" href="([^"]+)"[^>]+>',
            r'<div class="[^"]+propertyItem">(?:\s*<div[^>]+>\s*\w*\s*)*<\/div>\s*<div[^>]+>\s*<a[^>]+href="([^"]+)">',
            r'<div class="[^"]+listing[^"]+">\s*<a href="([^"]+)"[^>]+>',
            r'<a href="(\/real\-estate\/[^"]+)"[^>]+>',
            r'<a href="([^"]+\/listing\/[^"]+)"[^>]+>',
            r'<a[^>]+id="property\-[^"]+"[^>]+href="([^"]+)">',
            r',\s*"get_absolute_url":\s*"([^"]+)",',
            r'<a itemprop="url" href="([^"]+)"><figure>',
            r'<a[^>]+class="property[^"]+" href="([^"]+)">',
            r'<a href="(\/listings\/[^"]+)">',
            r'<a href="([^"]+)"[^>]+>View Property',
            r'<div class="[^"]+listing\-card[^"]+">\s*<a href="([^"]+)"[^>]+>',
            r'<div .*? onclick="javascript:window.location.href=\'([^"\']+)',
            r'<a .*?href="(.*?\/listing\/[^"]+)".*?>',
            r'<a .*?href="(.*?\/listing-detail[^"]+)".*?>',
            r'<a class="img-container" href="([^"]+)".*?>',
            r'<section data\-ha\-element\-link=".*?(https.*?\/property\\\/[^"&}]+)',
            r'<a[^>]+href="([^"]+\/listings\/[^"]+)"><div class="listing-card"',
            r'<a .*?href="(\/products\/[^"]+)',
            r'<a [^>]*href="([^"]+)"[^>]*class="listing"',
            r'<a href="([^"]+\/listing\/[^"]+)"[^>]+>',
            r'<a href="([^"]*\/property\/[^"]+)"',
            r'<a class="contentWrapper" href="([^"]+)"',
            r'<div class="[^"]*propertyListWrapper[^"]*">\s*?<a href="([^"]+)"',
            r'<a [^>]*href="([^"]*\/sale\/[^"]+)"',
            r'<a [^>]*href="([^"]+)"[^>]*class="card"',
            r'<a href="([^"]+)" +class="property\-[^"]+">',
            r'<a href="([^"]*property_id[^"]+)"',
            r'<a [^>]*href="([^"]*\/sold\/[^"]+)"',
            r'<a href="([^"]*\/rental\/[^"]+)"',
            r'<a href="([^"]*property[^"]+\/\d+)"',
            r'<a href="([^"]*\/all-properties\/[^"]*)"',
            r'<div class="item-image">[\s\t\r\n]*<a href="([^"]+)">',
            r'<a href="([^"]*\/recent-purchases\/[^"]+)"',
            r'<a href="(house\/[^"]+)|(townhouse\/[^"]+)|(land\/[^"]+)|(apartment\/[^"]+)|(villa\/[^"]+)"',
            r'<div class="[^"]*propertyListItemWrapper[^"]*"[^>]*>[\s\t\r\n]*<a href="([^"]+)"',
            r'<a .*?href="([^"]*\/listing\/[^"]+)".*?>',
            r'<section class="[^"]*propertyListItemWrapper[^"]*"[^>]*>[\s\t\r\n]*<a [^>]*href="([^"]+)"',
            r'<article class="[^"]*property[^"]*"[^>]*>[\s\t\r\n]*<a [^>]*href="([^"]+)"',
            r'<a [^>]*href="([^"]*\/sale\/[^"]+)"',
            r'<a href="(\/For\-Sale\/[^"]+)"',
            r'<a href="([^"]*\/for\-sale\/[^"]+)"',
            r'<a href="([^"]*\/sold\-properties\/[^"]+)"',
            r'<a href="([^"]*\/for\-lease\/[^"]+)"',
            r'<a href="([^"]*\/listing\?listing_id=\d+)"',
            r'<div class="[^"]+listing[^"]+">\s*<a href="([^"]+)"[^>]+>',
            r'<a [^>]*href="([^"]*\/listings\/[^"]*)"',
            r'<a [^>]*href="(\/buy\/[^"]+)"',
            r'<a [^>]*href="(\/rent\/[^"]+)"',
            r'<a [^>]*href="(\/sold\/[^"]+)"',
            r'<a [^>]*href="([^"]*?type=buy[^"]*)"',
            r'<a [^>]*href="([^"]*?type=rent[^"]*)"',
            r'<a [^>]*href="([^"]*\/commercial\/[^"]*)"',
            r'<a [^>]*href="([^"]*\/property\/[^"]+)"',
            r'<a[\s\t\r\n]*class="property\-card[^"]*"[\s\t\r\n]*href="([^"]+)"',
            r'<a [^>]*href="([^"]*\/sale\/[^"]+)"',
            r'<a [^>]*href="([^"]*\/lease\/[^"]+)"',
            r'<figcaption class="wp-element-caption">(?:<strong>)*[\s\t\r\n]*<a href="([^"]+)"',
            r'<div ga-event-key="property"[^>]*ga-event-label="([^"]+)"',
            r'<div class="listings-item">[\s\t\r\n]*<a href="([^"]+)"',
            r'<a class="" href="(propertydetails[^"]+)"',
            r'<a class="container display-block [^"]*" href="([^"]+)"',
            r'<div class="listing-item[^"]*">[\s\t\r\n]*<a href="([^"]+)"',
            r'<a href="([^"]+)" itemprop="url"\s*>',
            r'<a href="([^"]+)" [^>]*>View Listing</a>',
        ]:
            result = self.regex_match(regex, multi=True)
            if result:
                return result

    def extract_urls(self):
        urls = self.get_urls()
        if urls:
            urls = [get_url(self.base_url, url) for url in urls]
            urls = list(set(urls))
            return urls
        return []
