from web_crawler.web_crawler.spiders.article_spider import ArticleSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

def run_crawler(max_pages=100, max_depth=3):

    if os.path.exists('docs.csv'):
        os.remove('docs.csv')

    settings = get_project_settings()
    settings.set('DEPTH_LIMIT', max_depth)
    settings.set('CLOSESPIDER_PAGECOUNT', max_pages)

    process = CrawlerProcess(settings)
    process.crawl(ArticleSpider)
    process.start()

