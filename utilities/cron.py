from sys import argv
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def run(spider_name):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_name)
    process.start()


if __name__ == '__main__':
    spider_name = argv[1]
    run(spider_name)
