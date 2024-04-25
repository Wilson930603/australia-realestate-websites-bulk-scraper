from crawldata.helpers.utils import get_url
from crawldata.helpers.datapoints.base import BaseExtract


class PagingUrl(BaseExtract):
    def get_next(self):
        regex = self.regex_list.get('page')
        if regex:
            result = self.regex_match(regex)
            if result:
                return result
        for regex in [
            r'<a class="page-link" href="([^"]+)" rel="next"[^>]+>',
            r'<a class="sd next" href="([^"]+)">',
            r'"propertiesData":{"count":\d+,"next":"([^"]+)",',
            r'"count":\s*\d+,\s*"next":\s*"<a href="([^"]+)"[^>]+>',
            r'<li class="next">\s*<a href="([^"]+)">',
            r'<div class="next"><a href="([^"]+)"[^>]+>',
            r'<a class="next page\-numbers" href="([^"]+)">',
            r'<a class="[^"]+" id="load\-more"[^>]+href="([^"]+)">Load More',
            r'<a id="pagination\-next" class="next" href="([^"]+)"[^>]+>next',
            r"<a class='page-link' href='([^']+)'><i class=\"pro-chevron-right\">",
            r'<a href="([^"]+)" class="pagination\-item next">',
            r'<a class="nextpostslink" rel="next" href="([^"]+)"',
            r'<a class="next_page_link" href="([^"]+)"',
            r'<li class="page\-item">\s*<a class="page\-link active"[^>]+>\d+<\/a>\s*<\/li>\s*<li class="page\-item">\s*<a class="page\-link " href="([^"]+)">',
            r'<li class="active"><a[^>]+>\d+<\/a><\/li><li><a href="([^"]+)">',
            r'<a href="([^"]+)">\s*<li[^>]+>&gt;',
            r'<a class="direction next" href="([^"]+)" title="Next Page">',
            r'<a href="([^"]*page=\d+)">Next<\/a>',
            r'<a href="(\?page=\d+)" class="next[^"]+">Next<\/a>',
            r"<a href='([^']+)'><i class=\"fa fa\-chevron\-right\">",
            r'<a href="([^"]+)"[^>]+>▶<\/a>',
            r'<button\s*class="[^"]+"\s*hx\-get="([^"]+)"\s*',
            r'<a href="([^"]+)" class=next>Next',
        ]:
            result = self.regex_match(regex)
            if result:
                return result
    
    def extract_next_page(self):
        next_url = self.get_next()
        if next_url:
            return get_url(self.base_url, next_url)
        return None
