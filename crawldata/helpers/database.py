import os
import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy.sql import text


class Database:
    def __init__(self):
        load_dotenv()
        engine = sqlalchemy.create_engine(
            'mysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
                os.getenv('DB_USER'),
                os.getenv('DB_PASS'),
                os.getenv('DB_HOST'),
                os.getenv('DB_PORT'),
                os.getenv('DB_NAME')
            )
        )
        self.conn = engine.connect()
        self.create_tables()
    
    def create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS property_listing_urls_temp (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `business_id` VARCHAR(255),
                `search_type` VARCHAR(10),
                `url_found` TEXT,
                `server_id` INT,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `status` VARCHAR(15) DEFAULT 'PENDING'
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS listing_stats (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `business_id` VARCHAR(255),
                `search_type` VARCHAR(10),
                `url` TEXT,
                `domain` TEXT,
                `properties_found` INT,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS listing_stats_temp (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `business_id` VARCHAR(255),
                `search_type` VARCHAR(10),
                `url` TEXT,
                `domain` TEXT,
                `properties_found` INT,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS property (
                `hash_content` VARCHAR(32) PRIMARY KEY,
                `hash_url` VARCHAR(32),
                `business_id` VARCHAR(255),
                `search_type` VARCHAR(10),
                `html_path` VARCHAR(50),
                `url` TEXT,
                `address` VARCHAR(255),
                `suburb` VARCHAR(100),
                `state` VARCHAR(100),
                `price` VARCHAR(50),
                `description` TEXT,
                `images` TEXT,
                `bedrooms` VARCHAR(20),
                `bathrooms` VARCHAR(20),
                `carspaces` VARCHAR(20),
                `property_type` VARCHAR(30),
                `land_size` VARCHAR(20),
                `agent_name` TEXT,
                `agent_image` TEXT,
                `agent_phone` TEXT,
                `agent_email` TEXT,
                `latitude` VARCHAR(30),
                `longitude` VARCHAR(30),
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS property_images (
                `property_hash` VARCHAR(32),
                `hash_url` VARCHAR(32),
                `url` TEXT,
                `path` VARCHAR(50),
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (property_hash, hash_url),
                FOREIGN KEY (property_hash) REFERENCES property(hash_content)
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS daily_cron_stats (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `server_ip` VARCHAR(20),
                `listing_start_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                `listing_end_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                `property_start_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                `property_end_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                `buy_property_cnt` INT,
                `rent_property_cnt` INT,
                `sold_property_cnt` INT
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS search_keys_listings (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `website` VARCHAR(255),
                `search_type` VARCHAR(10),
                `site_path` TEXT,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `listing_url` TEXT,
                `listing_spider_type` VARCHAR(20),
                `pagination_xpath` VARCHAR(100)
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS regex_points (
                `website` VARCHAR(255) PRIMARY KEY,          
                `buy` TEXT,
                `sold` TEXT,
                `rent` TEXT, 
                `property` TEXT,
                `page` TEXT,
                `address` TEXT,
                `suburb` TEXT,
                `state` TEXT,
                `price` TEXT,
                `description` TEXT,
                `images` TEXT,
                `bedrooms` TEXT,
                `bathrooms` TEXT,
                `carspaces` TEXT,
                `property_type` TEXT,
                `land_size` TEXT,
                `agent_name` TEXT,
                `agent_image` TEXT,
                `agent_phone` TEXT,
                `agent_email` TEXT,
                `latitude` TEXT,
                `longitude` TEXT
            )                  
        """)

    def get_unchecked_urls(self):
        result = self.conn.execute("""
            SELECT website, business_spider_type as type FROM business_listings
            WHERE url_checked = 0 and website is not null
        """)
        return [dict(row) for row in result]

    def update_url_checked(self, url, row):
        # `url_checked` = 1, add later
        self.conn.execute(
            text("""
                UPDATE business_listings SET
                    `buy_listings_url` = :buy_listings_url,
                    `rent_listings_url` = :rent_listings_url,
                    `sold_listings_url` = :sold_listings_url
                WHERE `website` = :website and `url_checked` = 0;
            """),
            buy_listings_url=row['buy_listings_url'],
            rent_listings_url=row['rent_listings_url'],
            sold_listings_url=row['sold_listings_url'],
            website=url
        )
    
    def update_url_checked_error(self, url, note):
        self.conn.execute(
            text("""
                UPDATE business_listings SET
                    `note` = :note
                WHERE `website` = :website and `url_checked` = 0;
            """),
            note=note,
            website=url
        )
    
    def update_business_with_listing(self, listing_id, note):
        self.conn.execute(
            text("""
                UPDATE business_listings SET
                    `note` = :note
                WHERE `id` = :id;
            """),
            note=note,
            id=listing_id
        )

    def load_listings(self):
        result = self.conn.execute("""
            SELECT id, buy_listings_url, rent_listings_url, sold_listings_url, listing_spider_type as type, pagination_xpath
            FROM business_listings WHERE website is not null and (
                buy_listings_url is not null or 
                rent_listings_url is not null or 
                sold_listings_url is not null
            )
            and (note is null or note = 'ok' or note = '')
        """)
        return [dict(row) for row in result]

    def load_search_keys(self):
        result = self.conn.execute("""
            SELECT website, search_type, site_path, listing_url, listing_spider_type as type, pagination_xpath FROM search_keys_listings
        """)
        return [dict(row) for row in result]

    def purge_temp_property(self, server_id):
        self.conn.execute(
            text("""
                DELETE FROM property_listing_urls_temp WHERE server_id = :server_id;
            """),
            server_id=server_id
        )

    def update_temp_property(self, server_id):
        self.conn.execute(
            text("""
                UPDATE property_listing_urls_temp SET status = 'PROCESSING' WHERE server_id = :server_id;
            """),
            server_id=server_id
        )

    def load_property_temp(self, server_id):
        result = self.conn.execute(
            text("""
                SELECT p.business_id, p.search_type, p.url_found, b.property_spider_type as type
                from property_listing_urls_temp p, business_listings b where p.business_id = b.id and p.server_id = :server_id
            """),
            server_id=server_id
        )
        return [dict(row) for row in result]

    def insert_temp_property(self, rows):
        query = text("""
            INSERT INTO property_listing_urls_temp (
                `business_id`,
                `search_type`,
                `url_found`,
                `server_id`
            ) VALUES (
                :business_id,
                :search_type,
                :url_found,
                :server_id
            );
        """)
        self.conn.execute(query, rows)


    def load_daily_listing(self):
        result = self.conn.execute("""
            SELECT id, website, buy_listings_url, rent_listings_url, sold_listings_url FROM business_listings
            WHERE SUBSTRING_INDEX(SUBSTRING_INDEX(website, '://', -1), '/', 1) NOT IN (
                SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(url, '://', -1), '/', 1) FROM listing_stats
                    UNION ALL
                SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(url, '://', -1), '/', 1) FROM listing_stats_temp
            ) AND note IS NULL AND buy_listings_url IS NOT NULL ORDER BY website DESC
            limit 100
        """)
        return [dict(row) for row in result]


    def insert_listing_stats(self, row):
        self.conn.execute(
            text("""
                INSERT INTO listing_stats (
                    `business_id`,
                    `search_type`,
                    `url`,
                    `domain`,
                    `properties_found`
                ) VALUES (
                    :business_id,
                    :search_type,
                    :url,
                    :domain,
                    :properties_found
                );
            """),
            **row
        )


    def insert_listing_stats_temp(self, row):
        self.conn.execute(
            text("""
                INSERT INTO listing_stats_temp (
                    `business_id`,
                    `search_type`,
                    `url`,
                    `domain`,
                    `properties_found`
                ) VALUES (
                    :business_id,
                    :search_type,
                    :url,
                    :domain,
                    :properties_found
                );
            """),
            **row
        )


    def insert_property(self, row):
        self.conn.execute(
            text("""
                INSERT IGNORE INTO property (
                    `hash_content`,
                    `hash_url`,
                    `business_id`,
                    `search_type`,
                    `url`,
                    `address`,
                    `suburb`,
                    `state`,
                    `price`,
                    `description`,
                    `images`,
                    `bedrooms`,
                    `bathrooms`,
                    `carspaces`,
                    `property_type`,
                    `land_size`,
                    `agent_name`,
                    `agent_image`,
                    `agent_phone`,
                    `agent_email`,
                    `latitude`,
                    `longitude`
                ) VALUES (
                    :hash_content,
                    :hash_url,
                    :business_id,
                    :search_type,
                    :url,
                    :address,
                    :suburb,
                    :state,
                    :price,
                    :description,
                    :images,
                    :bedrooms,
                    :bathrooms,
                    :carspaces,
                    :property_type,
                    :land_size,
                    :agent_name,
                    :agent_image,
                    :agent_phone,
                    :agent_email,
                    :latitude,
                    :longitude
                );
            """),
            **row
        )

    def insert_property_images(self, row):
        self.conn.execute(
            text("""
                INSERT IGNORE INTO property_images (
                    `property_hash`,
                    `hash_url`,
                    `url`,
                    `path`
                ) VALUES (
                    :property_hash,
                    :hash_url,
                    :url,
                    :path
                );
            """),
            **row
        )

    def update_sites(self, site, values):
        self.conn.execute(
            text(f"""
                UPDATE business_listings SET
                    `business_spider_type` = :business_spider_type,
                    `listing_spider_type` = :listing_spider_type,
                    `property_spider_type` = :property_spider_type,
                    `pagination_xpath` = :pagination_xpath
                WHERE `website` like '{site}%';
            """),
            **values
        )

    def update_sub_sites(self, site, values):
        self.conn.execute(
            text(f"""
                UPDATE search_keys_listings SET
                    `listing_spider_type` = :listing_spider_type,
                    `pagination_xpath` = :pagination_xpath
                WHERE `website` like '{site}%';
            """),
            **values
        )

    def update_pages(self, business_id, pages):
        self.conn.execute(
            text("""
                UPDATE business_listings SET
                    `has_page` = :pages
                WHERE `id` = :business_id;
            """),
            pages=pages,
            business_id=business_id
        )

    def insert_daily_cron_stats(self, row):
        self.conn.execute(
            text("""
                INSERT INTO daily_cron_stats (
                    `server_ip`,
                    `listing_start_at`,
                    `listing_end_at`,
                    `property_start_at`,
                    `property_end_at`,
                    `buy_property_cnt`,
                    `rent_property_cnt`,
                    `sold_property_cnt`
                ) VALUES (
                    :server_ip,
                    :listing_start_at,
                    :listing_end_at,
                    :property_start_at,
                    :property_end_at,
                    :buy_property_cnt,
                    :rent_property_cnt,
                    :sold_property_cnt
                );
            """),
            **row
        )
    
    def load_listing_regex(self):
        result = self.conn.execute("""
            SELECT website, buy, sold, rent FROM regex_points;
        """)
        result = [dict(row) for row in result]
        rows = {}
        for row in result:
            rows[row['website']] = row
        return rows

    def load_property_regex(self):
        result = self.conn.execute("""
            SELECT website, property, page FROM regex_points;
        """)
        result = [dict(row) for row in result]
        rows = {}
        for row in result:
            rows[row['website']] = row
        return rows

    def load_data_regex(self):
        result = self.conn.execute("""
            SELECT
                website, address, suburb, state, price, description, images, bedrooms,
                bathrooms, carspaces, property_type, land_size, agent_name, agent_image,
                agent_phone, agent_email, latitude, longitude
            FROM regex_points;
        """)
        result = [dict(row) for row in result]
        rows = {}
        for row in result:
            rows[row['website']] = row
        return rows

    def insert_regex_points(self, row):
        self.conn.execute(
            text("""
                INSERT INTO regex_points (
                    `website`,
                    `buy`,
                    `sold`,
                    `rent`,
                    `property`,
                    `page`,
                    `address`,
                    `suburb`,
                    `state`,
                    `price`,
                    `description`,
                    `images`,
                    `bedrooms`,
                    `bathrooms`,
                    `carspaces`,
                    `property_type`,
                    `land_size`,
                    `agent_name`,
                    `agent_image`,
                    `agent_phone`,
                    `agent_email`,
                    `latitude`,
                    `longitude`
                ) VALUES (
                    :website,
                    :buy,
                    :sold,
                    :rent,
                    :property,
                    :page,
                    :address,
                    :suburb,
                    :state,
                    :price,
                    :description,
                    :images,
                    :bedrooms,
                    :bathrooms,
                    :carspaces,
                    :property_type,
                    :land_size,
                    :agent_name,
                    :agent_image,
                    :agent_phone,
                    :agent_email,
                    :latitude,
                    :longitude
                )
                ON DUPLICATE KEY UPDATE
                    `website` = VALUES(`website`),
                    `buy` = VALUES(`buy`),
                    `sold` = VALUES(`sold`),
                    `rent` = VALUES(`rent`),
                    `property` = VALUES(`property`),
                    `page` = VALUES(`page`),
                    `address` = VALUES(`address`),
                    `suburb` = VALUES(`suburb`),
                    `state` = VALUES(`state`),
                    `price` = VALUES(`price`),
                    `description` = VALUES(`description`),
                    `images` = VALUES(`images`),
                    `bedrooms` = VALUES(`bedrooms`),
                    `bathrooms` = VALUES(`bathrooms`),
                    `carspaces` = VALUES(`carspaces`),
                    `property_type` = VALUES(`property_type`),
                    `land_size` = VALUES(`land_size`),
                    `agent_name` = VALUES(`agent_name`),
                    `agent_image` = VALUES(`agent_image`),
                    `agent_phone` = VALUES(`agent_phone`),
                    `agent_email` = VALUES(`agent_email`),
                    `latitude` = VALUES(`latitude`),
                    `longitude` = VALUES(`longitude`)
                ;
            """),
            **row
        )
