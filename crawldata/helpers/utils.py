import json
import hashlib
from time import time


def hash(input):
    result = hashlib.md5(input.encode())
    return result.hexdigest()


def hash_url(url):
    return hash(url)


def hash_json(data):
    content = json.dumps(data)
    return hash(content)


def json_text(data):
    for key, value in data.items():
        if not value:
            data[key] = ''
        elif type(value) == list:
            data[key] = json.dumps(value)
    return data


def saving_log(data, name):
    rows = []
    if data.get('start_time'):
        rows.append(f'Start time: {data["start_time"]}')
    for keys in list(data.keys()):
        if keys in ['start_time', 'end_time']:
            continue
        rows.append(f'Count for {keys}: {data[keys]}')
    if data.get('end_time'):
        rows.append(f'End time: {data["end_time"]}')
    with open(f'logs/{name}/{int(time())}.txt', 'w') as f:
        f.write('\n'.join(rows))
    with open(f'logs/{name}.json', 'w') as f:
        json.dump(data, f)


def final_log(server_ip):
    with open(f'logs/listing.json', 'r') as f:
        listing = json.load(f)
    with open(f'logs/property.json', 'r') as f:
        property = json.load(f)
    data = {
        'server_ip': server_ip,
        'listing_start_at': listing['start_time'],
        'listing_end_at': listing['end_time'],
        'property_start_at': property['start_time'],
        'property_end_at': property['end_time'],
        'buy_property_cnt': listing['BUY'],
        'rent_property_cnt': listing['RENT'],
        'sold_property_cnt': listing['SOLD'],
    }
    return data


def extract_shema(url):
    return url.split('://', 1)[0]


def extract_base(url):
    schema, domain = url.split('://', 1)
    domain = domain.split('/')[0]
    return f'{schema}://{domain}'


def get_url(base, url):
    if not url:
        return None
    if url.startswith('http'):
        return url
    if url.startswith('//'):
        schema = extract_shema(base)
        return f'{schema}:{url}'
    if url.startswith('/'):
        domain = base.split('//')[1].split('/')[0]
        return f'{base.split(domain)[0]}{domain}{url}'
    else:
        return f'{base}/{url}'


def clean_url(url):
    if url:
        return url.replace('&#038;', '&').replace('&amp;', '&').replace('\\u0026', '&')
    return url


def extract_domain(url):
    if url:
        return url.split('//')[1].split('/')[0]
    return url


def clean_duplicates(data):
    urls = []
    final_data = []
    for item in data:
        url_buy = item.get('buy_listings_url')
        if url_buy and url_buy not in urls:
            urls.append(url_buy)
        else:
            item['buy_listings_url'] = None
        url_rent = item.get('rent_listings_url')
        if url_rent and url_rent not in urls:
            urls.append(url_rent)
        else:
            item['rent_listings_url'] = None
        url_sold = item.get('sold_listings_url')
        if url_sold and url_sold not in urls:
            urls.append(url_sold)
        else:
            item['sold_listings_url'] = None
        final_data.append(item)
    return final_data


def extra_points(base_url):
    try:
        file = open('notes.json', 'r')
        data = json.load(file)
        file.close()
    except:
        data = {}
    return data.get(base_url, {})


def server_info():
    try:
        return json.load(open('config.json', 'r'))
    except:
        return {
            "NumberOfServers": 1,
            "CurrentServer": 1,
            "ServerIP": "Undefined"
        }


def sites_run():
    try:
        return open('list.txt', 'r').read().splitlines()
    except:
        return []


def load_regex():
    try:
        return json.load(open('regex.json', 'r'))
    except:
        return {}
