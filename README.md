# Installation process
1. Install python 3.7.4 or above.
2. Clone the repository.
3. Install requirements.txt using `pip install -r requirements.txt`.
4. Download [chromedriver](https://chromedriver.chromium.org/downloads) and put it in the root folder.


# Configure the database
1. Make a copy of the file `.env.example` and name it `.env`.
2. Populate the database informations.
```
DB_HOST=<DB_HOST>
DB_USER=<DB_USER>
DB_PASS=<DB_PASS>
DB_NAME=<DB_NAME>
DB_PORT=<DB_PORT>
```
3. Copy the file inside the both `crawldata` folder and `Maps Scraping` in order to use the database.


# Additional configuration
If you're running the spider on multiple machines, you need to configure the `config.json` file.
Edit the file `config.json` and add the `CurrentServer`, `NumberOfServers` and `ServerIP` parameters.
```
{
    "NumberOfServers": 3,
    "CurrentServer": 1,
    "ServerIP": "127.0.0.1"
}
```


# Maps Spider
## Populating the suburbs
1. Go inside the `Maps Scraping` folder using `cd "Maps Scraping"`.
2. Put the suburbs inside the file `Suburbs_in_Australia.xlsx`.
3. Run the population script `python3 suburbs.py`.

## Running the spider (get businesses from Google Maps)
1. Go inside the `Maps Scraping` folder using `cd "Maps Scraping"`.
2. Run the spider `python3 maps.py`.


# Website Spiders
## Spider 1: business spider
This spider takes a list of businesses found from Google Maps (from the database) and tries to find the listings urls for each business. The `buy`, `sold` and `rent` urls. To run it: `scrapy crawl business`.


## Spider 2: listing spider
The spider takes a list of listings urls (from the database) and tries to scrape the data from each listing. The data scraped would be the `urls for the properties`. To run it: `scrapy crawl listing`.
This script also handles sub-listings if populated correctly.


## Spider 3: property spider
The spider takes a list of property urls (from the database) and tries to scrape the data from each property. To run it: `scrapy crawl property`.


## Spider 4: ripe spider
This spider is for testing purposes. It has 3 modes:
1. You provide the business url to get the listings urls `scrapy crawl ripe -a "website_url=https://example.com/"`.
2. You provide the listings url to get the properties urls `scrapy crawl ripe -a "business_listing_url=https://example.com/buy/"`.
3. You provide the property url to get the data points `scrapy crawl ripe -a "property_url=https://example.com/property/123"`.

If you want to use `selenium` in any of the above, add the parameter `-a selenium=True`.
After each run, you'll find the output in `ripe.csv`.


# Scripts
## Mark Selenium parts for the sites and subsites
1. Populate `sites.json` and run `python3 update_sites.py`.
2. The format needs to be as below:
```
{
    "listings": {
        "https://SITE1": {
            "business_spider_type": "selenium",
            "listing_spider_type": "selenium",
            "property_spider_type": null,
            "pagination_xpath": "//a[@title=\"View More Listings\"]"
        },
        "https://SITE2": {
            "business_spider_type": null,
            "listing_spider_type": null,
            "property_spider_type": "selenium",
            "pagination_xpath": null
        }
    },
    "sub_listings": {
        "https://SUBSITE1": {
            "listing_spider_type": "selenium",
            "pagination_xpath": "//a[@title=\"View More Listings\"]"
        },
        "https://SUBSITE2": {
            "listing_spider_type": null,
            "pagination_xpath": null
        }
    }
}
```

## Mark sites that have pagination
1. Populate `pages.json` and run `python3 update_sites.py`.
2. The format needs to be as below:
```
{
    "BUSINESS_ID_01": 1,
    "BUSINESS_ID_02": 0,
    "BUSINESS_ID_03": 1,
    "BUSINESS_ID_04": 0,
}
```

## Update regex for pages
1. Populate `regex.json` and run `python3 update_regex.py`.
2. The format needs to be as below:
```
{
    "SITE1": {
        "buy": "regex_buy_listing",
        "sold": "regex_sold_listing,
        "rent": "regex_rent_listing",
        "property": "regex_property_link",
        "page": "regex_next_page_link",
        "address": "regex_address_data",
        "suburb": "regex_suburb_data",
        "state": "regex_state_data",
        "price": "regex_price_data",
        "description": "regex_description_data",
        "images": "regex_images_data",
        "bedrooms": "regex_bedrooms_data",
        "bathrooms": "regex_bathrooms_data",
        "carspaces": "regex_carspaces_data",
        "property_type": "regex_property_type_data",
        "land_size": "regex_land_size_data",
        "agent_name": "regex_agent_name_data",
        "agent_image": "regex_agent_image_data",
        "agent_phone": "regex_agent_phone_data",
        "agent_email": "regex_agent_email_data",
        "latitude": "regex_latitude_data",
        "longitude": "regex_longitude_data",
    },
    "SITE2: {
        ...
    },
    ...
}
```


# Cronjob
## Cronjob for Google Maps Scraping
Setup using `crontab` with the format `? ? ? ? ? cd LOCATION && python3 maps.py`.

## Cronjob for Scrapy Spiders
Setup using `crontab` with the format `? ? ? ? ? cd LOCATION && python3 cron.py spider_name`.


# Logging
The main spiders `business`, `listing` and `property` have some logs saved inside the folder `logs` with the timestamp of the run.
```
logs
├── business
│   ├── 1695225630.txt
│   ├── 1695493171.txt
│   ├── 1695519711.txt
│   ├── 1695606692.txt
│   ├── 1695610866.txt
│   ├── 1695693120.txt
│   └── 1695779112.txt
├── listing
│   ├── 1695294322.txt
│   ├── 1695493827.txt
│   ├── 1695529226.txt
│   ├── 1695957071.txt
│   └── 1696053061.txt
└── property
    ├── 1695482366.txt
    ├── 1695502612.txt
    └── 1695655922.txt
```
Some logs are also saved in the database in the table `daily_cron_stats`.


# Database Tables
## Table: `suburbs`
This has the list of suburbs in Australia. It's populated using the `Suburbs_in_Australia.xlsx` file.

## Table: `business_listings`
This has the list of businesses found from Google Maps. It's populated using the `maps.py` script.

## Table: `listing_stats`
This has the list of listings urls found from the businesses. It's populated using the spider `listing`.

## Table: `property`
This has the list of properties urls found from the listings. It's populated using the spider `property`.

## Table: `property_listing_urls_temp`
This has the list of properties urls found from the listings. It's populated using the spider `listing`.

## Table: `property_images`
This has the list of images urls found from the properties. It's populated using the spider `property`.

## Table: `search_keys_listings`
This has the list of search keys used to find the listings urls for sub-listings.

## Table: `regex_points`
This has the list of regex points used to scrape the data from the listings and properties. It's populated using the `update_regex.py` script.
