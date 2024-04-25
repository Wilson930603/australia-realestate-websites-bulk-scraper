import os
import json
import requests
import traceback
from time import sleep
from threading import Lock
from database import Database
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys


def get_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument("--incognito")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--ssl-client-certificate-file=ca.crt')
    options.add_argument('--lang=en')
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option('useAutomationExtension', False) 
    browser = webdriver.Chrome(
        service_log_path=os.devnull,
        options=options,
        seleniumwire_options=None
    )
    return browser


def visit(browser, search_text):
    browser.get('https://www.google.com/maps/@-30.7229487,146.8981935,5z?hl=en&entry=ttu')
    sleep(5)
    search_box = browser.find_element_by_css_selector('input#searchboxinput')
    search_box.send_keys(search_text)
    search_box.send_keys(Keys.ENTER)
    sleep(5)
    browser.requests.clear()
    search_box.send_keys(Keys.ENTER)
    sleep(5)
    need_scroll = True
    nb_elements = 0
    tries = 0
    while need_scroll:
        el = browser.find_element_by_css_selector('[role="feed"]')
        if el:
            new_nb_elements = len(browser.find_elements_by_css_selector('[role="feed"] > div'))
            if new_nb_elements != nb_elements:
                tries = 0
                nb_elements = new_nb_elements
            browser.execute_script("arguments[0].scrollBy(0, arguments[0].scrollHeight)", el)
            sleep(1)
        else:
            need_scroll = False
        try:
            end = browser.find_element_by_css_selector('p.fontBodyMedium > span > span')
            if end:
                need_scroll = False
        except:
            tries += 1
            if tries == 30:
                1/0
            sleep(2)


def extract_urls(browser):
    urls = []
    for request in browser.requests:
        if request.response and 'search?tbm' in request.url:
            urls.append(request.url)
    return urls


def extract_data(urls, search_text):
    urls = list(set(urls))
    for url in urls:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        while True:
            try:
                response = requests.get(url, headers=headers)
                break
            except:
                sleep(5)
        resp_text = response.text.replace('/*""*/', '')
        data = json.loads(resp_text)
        data_d = data['d'][4:]
        data_d = json.loads(data_d)[0][1]
        for item in data_d[1:]:
            item_data = item[14]
            name = item_data[11]
            address = item_data[39]
            review_data = item_data[4]
            place_id = item_data[78]
            if review_data:
                rating = review_data[7]
                reviews = review_data[8]
            else:
                rating = None
                reviews = 0
            website = item_data[7][0] if item_data[7] else None
            try:
                tel = item_data[178][0][0]
            except:
                tel = None
            it = {
                'id': place_id,
                'search_text': search_text,
                'name': name,
                'address': address,
                'rating': rating,
                'reviews': reviews,
                'website': website,
                'tel': tel
            }
            try:
                print(it)
                db.insert_row(it)
            except:
                print(traceback.format_exc())


def process_one(search_text):
    global searched
    if search_text in searched:
        return
    browser = get_browser()
    try:
        visit(browser, search_text)
        urls = extract_urls(browser)
        extract_data(urls, search_text)
        lock_searched.acquire()
        with open('searched.txt', 'a') as f:
            f.write(search_text + '\n')
        lock_searched.release()
    except Exception as e:
        print(traceback.format_exc())
    browser.close()
    browser.quit()


db = Database()
processed = []
lock_searched = Lock()
texts_search = db.load_suburbs_search()
print(f'Number of texts to search: {len(texts_search)}')
finished = False
while not finished:
    try:
        searched = open('searched.txt', 'r').read().splitlines()
    except:
        searched = []
    texts_search = list(set(texts_search) - set(searched))
    print(f'Number of texts left to search: {len(texts_search)}')
    if not texts_search:
        finished = True
    for text_search in texts_search:
        try:
            process_one(text_search)
        except Exception as e:
            print(traceback.format_exc())
    sleep(5)
