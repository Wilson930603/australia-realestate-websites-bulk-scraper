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
        self.create_table()
    
    def create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS suburbs (
                `search_text` VARCHAR(255) PRIMARY KEY,
                `suburb` VARCHAR(255) NULL,
                `state` VARCHAR(255) NULL
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS business_listings (
                `id` VARCHAR(255) PRIMARY KEY,
                `name` VARCHAR(255) NULL,
                `address` VARCHAR(255) NULL,
                `tel` VARCHAR(255) NULL,
                `website` VARCHAR(500) NULL,
                `rating` VARCHAR(255) NULL,
                `reviews` VARCHAR(255) NULL,
                `search_text` VARCHAR(255) NULL,
                `buy_listings_url` TEXT,
                `rent_listings_url` TEXT,
                `sold_listings_url` TEXT,
                `country` VARCHAR(255) DEFAULT 'AUS',
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                `url_checked` TINYINT(1) DEFAULT 0,
                `note` TEXT,
                `has_page` INT(1) DEFAULT 0,
                `business_spider_type` VARCHAR(20),
                `listing_spider_type` VARCHAR(20),
                `property_spider_type` VARCHAR(20),
                `pagination_xpath` VARCHAR(100)
            )
        """)

    def insert_row(self, row):
        self.conn.execute(
            text("""
                INSERT INTO business_listings (
                    `id`,
                    `name`,
                    `address`,
                    `tel`,
                    `website`,
                    `rating`,
                    `reviews`,
                    `search_text`
                ) VALUES (
                    :id,
                    :name,
                    :address,
                    :tel,
                    :website,
                    :rating,
                    :reviews,
                    :search_text
                ) ON DUPLICATE KEY UPDATE
                    `tel` = VALUES(`tel`),
                    `rating` = VALUES(`rating`),
                    `reviews` = VALUES(`reviews`);
            """),
            **row
        )
    
    def insert_suburb(self, row):
        self.conn.execute(
            text("""
                INSERT IGNORE INTO suburbs (
                    `search_text`,
                    `suburb`,
                    `state`
                ) VALUES (
                    :search_text,
                    :suburb,
                    :state
                );
            """),
            **row
        )
    
    def load_suburbs_search(self):
        result = self.conn.execute("""
            SELECT search_text FROM suburbs
        """)
        return [row[0] for row in result]
