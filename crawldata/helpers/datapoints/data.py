import re
import json
from crawldata.helpers.utils import get_url
from crawldata.helpers.datapoints.base import BaseExtract


class crawlDatapoints(BaseExtract):
    def crawl_address(self):
        regex = self.regex_list.get('address')
        if regex:
            result = self.regex_match(regex)
            if result:
                return result
        for regex in [
            r"listing_location: '(.*?)'",
            r'"fullAddress":"(.*?)"',
            r'"property_address":"(.*?)"',
            r'"address":\s*"(.*?)"',
            r'<div class="residential-attributes-head">\s*<h2[^>]+>([^>]+)<',
            r'<input type="hidden" id="ListingAddress" name="ListingAddress" value="([^"]+)" \/>',
            r'<span class="address">(.*?)</span>',
            r'<[^>]*>Address<\/[^>]*>\s*<[^>]+>(.+)<\/[^>]+>',
            r'data\-address="([^"]+)"',
            r'<[^\s]+ class="[^"]+address" itemprop="name">([^<]+)<\/[^>]+>',
            r'<input .+ name="[^"]+address" value="([^"]+)">',
            r'"streetAddress":\s*"(.*?)"',
            r'<div class="[^"]*address">\n*(.+)<\/div>',
            r'<\w+ class="[^"]*address[^"]*">\n*([^<]+)<',
            r'<h1 [^>]+>([^<]+)<\/h1>',
            r"<textarea class='form-control' name='message' rows='3'>([^-]+) \-",
            r"{'address': '([^']+)'}",
        ]:
            result = self.regex_match(regex)
            if result:
                result = re.sub(r'<[^>]+>', '', result)
                result = result.strip()
                return result

    def crawl_suburb(self):
        regex = self.regex_list.get('suburb')
        if regex:
            result = self.regex_match(regex)
            if result:
                return result
        for regex in [
            r'"addressLocality": "(.*?)"',
            r'"suburb":"(.*?)",',
            r'&suburb\=\d+" class="[^"]+">(.+)<\/a>',
            r'<meta property="og:locality" content="([^"]+)" \/>',
        ]:
            result = self.regex_match(regex)
            if result:
                return result
    
    def crawl_suburb_from_address(self, address):
        for regex in [
            r"^(?:.*,)?\s*(.*?),\s*[A-Z]{2},?\s*\d{5}$",
            r'.+, (.+), \w{1,3} \d+$',
            r'.+,\s*(.+) \w{1,3} \d+$',
            r'.+,\s*(.+) \d+$',
            r'^[^,]+, ([^\d,]+)$',
        ]:
            result = self.regex_match(regex, address)
            if result:
                return result

    def crawl_state(self):
        regex = self.regex_list.get('state')
        if regex:
            result = self.regex_match(regex)
            if result:
                return result
        for regex in [
            r'"addressRegion": "(.*?)"',
            r'"state":"(.*?)",',
            r'&state\=(.*?)"',
            r'<meta property="og:region" content="([^"]+)" \/>',
        ]:
            result = self.regex_match(regex)
            if result:
                return result
    
    def crawl_state_from_address(self, address):
        for regex in [
            r"^(?:.*,)?\s*.*?,\s*([A-Z]{2}),?\s*\d{5}$",
            r'.+,\s*.+ (\w{1,3}) \d+',
            r'.+, (\w{1,3}) \d+ \w+$',
        ]:
            result = self.regex_match(regex, address)
            if result:
                return result

    def crawl_price(self):
        regex = self.regex_list.get('price')
        if regex:
            result = self.regex_match(regex)
            if result:
                return result
        for regex in [
            r'<div class="price[^"]+">(?:\s*<div[^>]+>)+\s*<h3>([^<]+)<\/h3>',
            r'<div class="price[^"]+">\s([^\n]+)',
            r'<[^>]*>Price<\/[^>]*>\s*<[^>]+>(.+)<\/[^>]+>',
            r'From ([0-9,]+)',
            r'\$([\$\-0-9,]{5,15})',
        ]:
            result = self.regex_match(regex)
            if result:
                return result

    def crawl_description(self):
        regex = self.regex_list.get('description')
        if regex:
            result = self.regex_match(regex)
            if result:
                return result
        for xpath in [
            '//div[@class="pdp_description_content"]//text()',
            '//div[@class="fusion-text fusion-text-7"]/p/text()',
            '//div[@class="details-text "]/p/text()',
            '//div[@class="section-body post-content"]/p/text()',
            '//div[@class="detail-description"]//text()',
            '//div[contains(@class, "property-details-description")]//text()',
            '//div[@class="single-listing__content listing-single__features wpb_animate_when_almost_visible fadeIn"]//text()',
            '//div/@data-description',
            '//div[@class="description"]//text()',
            '//div[@class="listing__description"]//text()',
            '//div[@class="propertycontents"]//text()',
            '//div[@itemprop="description"]/p/text()',
            '//div[@class="contentRegion"]/p//text()',
        ]:
            result = self.tree_match(xpath, multi=True)
            if result:
                result = '\n'.join(result)
                return result
        
        for regex in [r'"listingId":\d+,"description":"(.*?)"']:
            result = self.regex_match(regex)
            if result:
                return result

    def crawl_images(self):
        regex = self.regex_list.get('images')
        if regex:
            result = self.regex_match(regex, multi=True)
            if result:
                return result
        for xpath in ['//img/@src']:
            result = self.tree_match(xpath, multi=True)
            if result:
                return list(set(result))

    def crawl_bedrooms(self):
        regex = self.regex_list.get('bedrooms')
        if regex:
            result = self.regex_match(regex)
            if result:
                return result
        for regex in [
            r'<i class=".+-bedrooms"><\/i>\s*<span class=[^>]+>(\d+)<\/span>',
            r'<div class="listing-single__attr--value">([0-9]+)<\/div>\s*<[^>]*><.+bed1">',
            r'<div [^>]*>\s*<i class=".+-bed"><\/i>\s*<\/div>\s*<div [^>]*>\s*([0-9]+)',
            r'<span>(\d+) <img src="[^>]*bedrooms.png" alt="">',
            r'<\w+ class="[^"]+bed"><\/\w+>\s*<[^>]*>(\d+)<\/\w+>',
            r'<\w+>(\d+)<\w+ class="\w+-bed">',
            r'<[^>]*>Bedrooms<\/[^>]*>\s*<[^>]+>([0-9]+)<\/[^>]+>',
            r'listing_beds: (\d+),',
            r'(\d+) BED',
            r'(\d+) Bed',
            r'(\d+) bed',
            r'(\d+)-bed',
        ]:
            result = self.regex_match(regex)
            if result:
                return result
        for xpath in [
            '//*[@class="bed"]//text()',
            '//*[contains(@class, "bed")]/text()',
            '//*[contains(@class, "beds")]/span/text()',
        ]:
            result = self.tree_match(xpath)
            if result:
                return result

    def crawl_bathrooms(self):
        regex = self.regex_list.get('bathrooms')
        if regex:
            result = self.regex_match(regex)
            if result:
                return result
        for regex in [
            r'<i class=".+-bathrooms"><\/i>\s*<span class=[^>]+>(\d+)<\/span>',
            r'<div class="listing-single__attr--value">([0-9]+)<\/div>\s*<[^>]*><.+bath1">',
            r'<div [^>]*>\s*<i class=".+-bath"><\/i>\s*<\/div>\s*<div [^>]*>\s*([0-9]+)',
            r'<span>(\d+) <img src="[^>]*bathrooms.png" alt="">',
            r'<\w+ class="[^"]+bath"><\/\w+>\s*<[^>]*>(\d+)<\/\w+>',
            r'<\w+>(\d+)<\w+ class="\w+-bath">',
            r'<[^>]*>Bathrooms<\/[^>]*>\s*<[^>]+>([0-9]+)<\/[^>]+>',
            r'listing_baths: (\d+),',
            r'(\d+) BATH',
            r'(\d+) Bath',
            r'(\d+) bath',
            r'(\d+)-bath',
        ]:
            result = self.regex_match(regex)
            if result:
                return result
        for xpath in [
            '//*[@class="bath"]//text()',
            '//*[contains(@class, "bath")]/text()',
            '//*[contains(@class, "baths")]/span/text()',
        ]:
            result = self.tree_match(xpath)
            if result:
                return result

    def crawl_carspaces(self):
        regex = self.regex_list.get('carspaces')
        if regex:
            result = self.regex_match(regex)
            if result:
                return result
        for regex in [
            r'<i class=".+-garages"><\/i>\s*<span class=[^>]+>(\d+)<\/span>',
            r'<div class="listing-single__attr--value">([0-9]+)<\/div>\s*<[^>]*><.+park1">',
            r'<div [^>]*>\s*<i class=".+-car"><\/i>\s*<\/div>\s*<div [^>]*>\s*([0-9]+)',
            r'<span>(\d+) <img src="[^>]*garage.png" alt="">',
            r'<\w+ class="[^"]+car"><\/\w+>\s*<[^>]*>(\d+)<\/\w+>',
            r'<\w+>(\d+)<\w+ class="\w+-car">',
            r'<[^>]*>Carport<\/[^>]*>\s*<[^>]+>([0-9]+)<\/[^>]+>',
            r'<[^>]*>Garage<\/[^>]*>\s*<[^>]+>([0-9]+)<\/[^>]+>',
            r'Garage spaces: (\d+)',
            r'Lockable garage: (\d+)',
            r'listing_cars: (\d+),',
            r'(\d+) CAR',
            r'(\d+) Car',
            r'(\d+)-car',
            r'(Double remote garage)',
            r'(Double garage)',
            r'([0-9]+) secured parking for the occupant',
        ]:
            result = self.regex_match(regex)
            if result:
                if result in ['Double remote garage', 'Double garage']:
                    result = '2'
                if 'and visitors parking' in self.html_content:
                    try:
                        result = str(int(result) + 1)
                    except:
                        pass
                return result
        for xpath in [
            '//*[@class="car"]//text()',
            '//*[@class="carports"]//text()',
            '//*[contains(@class, "car") and not(contains(@class, "card"))]/text()',
            '//*[contains(@class, "cars")]/span/text()',
        ]:
            result = self.tree_match(xpath)
            if result:
                return result

    def crawl_property_type(self):
        regex = self.regex_list.get('property_type')
        if regex:
            result = self.regex_match(regex)
            if result:
                return result
        for regex in [
            r'"@context": "http://schema.org",\n  "@type": "(.+)",',
            r'<[^>]+>Property Type<\/[^>]+>\n\s*<[^>]+>([^<]+)<\/[^>]+>',
            r'>Property Type: ([^^<]+)<',
            r'\- (.+) For Sale \| ',
            r'<[^>]+>Property Type:<\/[^>]+>\s*([^<]+)',
            r'<div[^>]+>Property type<\/div><div[^>]+>([^>]+)<\/div>',
            r'<strong>Property Type<\/strong>: ([^>]+)<',
            r'<[^>]+>Property Type:<\/[^>]+>\s<[^>]+>([^<]+)<',
        ]:
            result = self.regex_match(regex)
            if result:
                return result

    def crawl_land_size(self):
        regex = self.regex_list.get('land_size')
        if regex:
            result = self.regex_match(regex)
            if result:
                return result
        for regex in [
            r'<strong>Land Size<\/strong>: ([^>]+)<',
            r'<[^>]+>\s*Land Size\s*<\/[^>]+>\n*\s*<[^>]+>\s*([^\/]+)<\/[^>]+>',
            r'<[^>]+>\s*Land area approx\s*<\/[^>]+>\n*\s*<[^>]+>\s*([^\/]+)<\/[^>]+>',
            r'<[^>]+>\s*Land size\s*<\/[^>]+>\n*\s*<[^>]+>\s*([^\/]+)<\/[^>]+>',
            r'<[^>]+>Land Area<\/[^>]+>\n\s+<[^>]+>([^<]+)<\/[^>]+>',
            r'<[^>]+>\s*Land\s*<\/[^>]+>\n*\s*<[^>]+>\s*([^\/]+)<\/[^>]+>',
            r'<[^>]+>\s*Land[\s\-!<>]*:<\/[^>]+><\/[^>]+><[^>]+><[^>]+>([^<]+)<\/[^>]+>',
            r'<[^>]+>land size<\/[^>]+>\s(.+)',
            r'Land \/ ([^<]+)',
            r'>Land Area: ([^^<]+)<',
            r'>Landsize : ([^<]+)<',
            r'>([0-9,\.]+m2)<',
            r'<li class="square-meters-container">\s*<span>([^\s]+)\s',
            r'<span[^>]+>Floor area approx<\/span>\s*<span[^>]+>([^>]+)<',
            r'<[^>]+>Land Area:<\/[^>]+>\s<[^>]+>([^<]+)<',
        ]:
            result = self.regex_match(regex)
            if result:
                result = result.replace('&nbsp;', '').replace('<sup>', '')
                result = re.sub(r'\s+', ' ', result)
                return result
    
    def crawl_agents(self):
        result = self.regex_match(r'"agents":(\[[^\]]+\])')
        if result:
            try:
                agents_names = []
                agents_phones = []
                agents_emails = []
                agents = json.loads(result)
                if type(agents) == list:
                    return [], [], [], False
                for agent in agents:
                    agents_names.append(agent['fullName'])
                    agents_phones.append(agent['mobilePhone'])
                    agents_emails.append(agent['email'])
                return json.dumps(agents_names), json.dumps(agents_phones), json.dumps(agents_emails), True
            except:
                return [], [], [], False
        return [], [], [], False
    
    def crawl_agent_name(self):
        regex = self.regex_list.get('agent_name')
        if regex:
            result = self.regex_match(regex, multi=True)
            if result:
                return result
        for regex in [
            r'"linkedin":"[^"]+","fullName":"([^"]+)",',
            r'"AGENT \| ([^",]+)"',
            r'See ([^\']+)\'s profile',
            r'<img src="[^"]+" alt="([^"]+)" class="[^"]+__agent-img">',
            r'<\w+ class="agentName">([^<]+)<\/\w+>',
            r'<\w+ class="listing-question__name"[^>]+>([^<]+)<\/\w+>',
            r'<\w+ class="agent">\n*\s*<\w+ class="name">([^<]+)',
        ]:
            result = self.regex_match(regex, multi=True)
            if result:
                return result
        call_text = self.regex_match(r'(Call [^!]+ to inspect!)')
        if call_text:
            result = self.regex_match(r'(Call | or )([a-zA-Z ]+) on [0-9]+', content=call_text, group=2, multi=True)
            if result:
                return result
        for xpath in [
            '(//div[@class="agents-container"])[2]/div/div/div/div/div[2]//a/span/text()',
            '//section[contains(@class, "single-listing-agents")]/div[2]/div/div[1]/h5/a/text()',
            '//div[@class="media-list consultant-list"]/div//h4/text()',
            '//div[@class="listing__agent_details__container"]/div/div/div[1]/div[1]/a/text()',
            '//div[@class="agent-name"]/div[2]/p/a[1]/text()',
        ]:
            result = self.tree_match(xpath, multi=True)
            if result:
                return result
    
    def crawl_agent_image(self):
        regex = self.regex_list.get('agent_image')
        if regex:
            result = self.regex_match(regex, multi=True)
            if result:
                return result
        for xpath in ['//*[contains(@class, "agent") or contains(@class, "Agent") or contains(@class, "consultant")]']:
            result = self.tree_match(xpath, multi=True)
            if result:
                result = self.tree_html(result)
                possible_images = []
                for row in result:
                    for regex in [
                        r'<img[^>]+src="[^"]+" data-src="([^"]+)"',
                        r'<img[^>]+src="([^"]+)"',
                        r'style="background\-image:\s*url\(\'?([^\']+)\'?\)"',
                    ]:
                        images = self.regex_match(regex, content=row, multi=True)
                        if images:
                            possible_images += images
                if possible_images:
                    return possible_images
        for regex in [
            r'<wow\-image [^>]+agent[^>]+><img src="([^"]+)"',
            r'<a class="agentImage"[^>]+style="background\-image: url\(\'[^\']+\'\)"',
        ]:
            result = self.regex_match(regex, multi=True)
            if result:
                return result

    def crawl_agent_phone(self):
        regex = self.regex_list.get('agent_phone')
        if regex:
            result = self.regex_match(regex, multi=True)
            if result:
                return result
        for xpath in ['//*[contains(@class, "agent")]']:
            result = self.tree_match(xpath, multi=True)
            if result:
                result = self.tree_html(result)
                possible_phones = []
                for row in result:
                    phones = self.regex_match(r'href="tel:([0-9\s\(\)]+)"', content=row, multi=True)
                    if phones:
                        possible_phones += phones
                if possible_phones:
                    return possible_phones
        for regex in [
            r'please call \w+ on ([0-9 ]+)',
            r'href="tel:([0-9\s\(\)]+)"',
            r'data\-phonenumber="([0-9\s\(\)]+)"',
            r'<\w+><\w+ class="[^"]+contact\-phone"><\/\w+>([0-9\s\(\)]+)<\/\w+>',
        ]:
            result = self.regex_match(regex, multi=True)
            if result:
                return result
        for regex in [
            r'<a class="[^"]+phone"[^>]+data\-id="([^"]+)"',
        ]:
            result = self.regex_match(regex, multi=True)
            if result:
                try:
                    return self.decode_phones(result)
                except:
                    pass
    
    def crawl_agent_email(self):
        regex = self.regex_list.get('agent_email')
        if regex:
            result = self.regex_match(regex, multi=True)
            if result:
                return result
        for xpath in ['//*[contains(@class, "agent")]']:
            result = self.tree_match(xpath, multi=True)
            if result:
                result = self.tree_html(result)
                possible_emails = []
                for row in result:
                    emails = self.regex_match(r'href="mailto:([^"]+@[^"]+)"', content=row, multi=True)
                    if emails:
                        possible_emails += emails
                if possible_emails:
                    return possible_emails
        for regex in [
            r'name="agent_email" value="([^"]+)"',
            r'href="mailto:([^"]+@[^"]+)"',
            r' value="([^"]+@[^"]+)" ',
        ]:
            result = self.regex_match(regex, multi=True)
            if result:
                return result

    def crawl_latitude(self):
        regex = self.regex_list.get('latitude')
        if regex:
            result = self.regex_match(regex)
            if result:
                return result
        for regex in [
            r'"latitude":\s*([0-9\.\-]+)',
            r'RexTemplate.postLat = ([0-9\.\-]+)',
            r'"coords":"([0-9\.\-]+), [0-9\.\-]+"',
            r'{"@type":"GeoCoordinates","latitude":"([0-9\.\-]+)","longitude":"[0-9\.\-]+"}',
            r'const position = { lat:\s*([0-9\.\-]+)\s*, lng:\s*[0-9\.\-]+\s*};',
            r'data-cord="([0-9\.\-]+),[0-9\.\-]+"',
            r'{"height":\d+,"latitude":"([0-9\.\-]+)","longitude":"[0-9\.\-]+","markerColor":',
            r',"default_lat":"([0-9\.\-]+)","default_lng":"[0-9\.\-]+",',
            r'center: \[([0-9\.\-]+),\s*[0-9\.\-]+\],',
            r'L.marker\(\[([0-9\.\-]+),\s*[0-9\.\-]+\]\)',
            r'<meta property="place:location:latitude" content="([0-9\.\-]+)" \/>',
        ]:
            result = self.regex_match(regex)
            if result:
                return result

    def crawl_longitude(self):
        regex = self.regex_list.get('longitude')
        if regex:
            result = self.regex_match(regex)
            if result:
                return result
        for regex in [
            r'"longitude":\s*([0-9\.\-]+)',
            r'RexTemplate.postLong = ([0-9\.\-]+)',
            r'"coords":"[0-9\.\-]+, ([0-9\.\-]+)"',
            r'{"@type":"GeoCoordinates","latitude":"[0-9\.\-]+","longitude":"([0-9\.\-]+)"}',
            r'const position = { lat:\s*[0-9\.\-]+\s*, lng:\s*([0-9\.\-]+)\s*};',
            r'data-cord="[0-9\.\-]+,([0-9\.\-]+)"',
            r'{"height":\d+,"latitude":"[0-9\.\-]+","longitude":"([0-9\.\-]+)","markerColor":',
            r',"default_lat":"[0-9\.\-]+","default_lng":"([0-9\.\-]+)",',
            r'center: \[[0-9\.\-]+,\s*([0-9\.\-]+)\],',
            r'L.marker\(\[[0-9\.\-]+,\s*([0-9\.\-]+)\]\)',
            r'<meta property="place:location:longitude" content="([0-9\.\-]+)" \/>',
        ]:
            result = self.regex_match(regex)
            if result:
                return result
    
    def clean(self, json_data):
        for key, value in json_data.items():
            if isinstance(value, str):
                json_data[key] = value.strip() if value else None
            elif isinstance(value, list):
                json_data[key] = [v.strip() if v else None for v in value]
                json_data[key] = [v for v in json_data[key] if v]
                marker = set()
                json_data[key] = [v for v in json_data[key] if v.lower() not in marker and not marker.add(v.lower())]
        return json_data

    def crawl(self):
        address = self.crawl_address()
        if address:
            address = address.replace(' ,', ',').replace(',,', ',')
        suburb = self.crawl_suburb()
        if address and not suburb:
            suburb = self.crawl_suburb_from_address(address)
        state = self.crawl_state()
        if address and not state:
            state = self.crawl_state_from_address(address)
        agent_names, agent_phones, agent_emails, success = self.crawl_agents()
        if not success:
            agent_names = self.crawl_agent_name()
            agent_phones = self.crawl_agent_phone()
            agent_emails = self.crawl_agent_email()
        agent_images = self.crawl_agent_image()
        if agent_images:
            agent_images = [get_url(self.base_url, img) for img in agent_images]
        images = self.crawl_images()
        if images:
            images = [get_url(self.base_url, img) for img in images]
        return self.clean({
            'address': address,
            'suburb': suburb,
            'state': state,
            'price': self.crawl_price(),
            'description': self.crawl_description(),
            'images': self.crawl_images(),
            'bedrooms': images,
            'bathrooms': self.crawl_bathrooms(),
            'carspaces': self.crawl_carspaces(),
            'property_type': self.crawl_property_type(),
            'land_size': self.crawl_land_size(),
            'agent_name': agent_names,
            'agent_image': agent_images,
            'agent_phone': agent_phones,
            'agent_email': agent_emails,
            'latitude': self.crawl_latitude(),
            'longitude': self.crawl_longitude(),
        })
