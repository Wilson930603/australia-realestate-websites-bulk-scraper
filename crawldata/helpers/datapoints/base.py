import re
from lxml import html
from base64 import b64decode


class BaseExtract:
    def __init__(self, html_content, base_url, regex_list):
        self.base_url = base_url
        self.html_content = html_content
        self.tree = html.fromstring(html_content)
        self.regex_list = regex_list

    def regex_match(self, regex, content=None, multi=False, group=1):
        if not content:
            content = self.html_content
        if multi:
            matches = re.finditer(regex, content, re.IGNORECASE)
            result_list = []
            for match in matches:
                result_list.append(match.group(group))
            return result_list if result_list else None
        else:
            result = re.search(regex, content, re.IGNORECASE)
            if result:
                return result.group(group)
            else:
                return None
    
    def tree_match(self, xpath, multi=False):
        result = self.tree.xpath(xpath)
        if result:
            if not multi:
                result = result[0].strip()
                if result:
                    return result
                else:
                    return None
            else:
                result = [x.strip() if type(x) == str else x for x in result]
                result = [x for x in result if x]
                if result:
                    return result
                else:
                    return None
        else:
            return None

    def tree_html(self, items):
        return [html.tostring(item).decode('utf-8').replace('%20', ' ') for item in items]
    
    def decode_phones(self, items):
        return [b64decode(item).decode('utf-8') for item in items]
