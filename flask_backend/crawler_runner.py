from web_crawler.web_crawler.spiders.article_spider import ArticleSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import subprocess

def run_crawler(max_pages=500, max_depth=50):

    if os.path.exists('docs.csv'):
        os.remove('docs.csv')

    settings = get_project_settings()
    settings.set('DEPTH_LIMIT', max_depth)
    settings.set('CLOSESPIDER_PAGECOUNT', max_pages)

    process = CrawlerProcess(settings)
    process.crawl(ArticleSpider)
    process.start()

def run_crawler_subprocess():

    # Construct the command to run the Scrapy crawler
    command = [
        'scrapy',
        'crawl',
        'article_spider'
    ]
    
    # Run the command as a subprocess
    subprocess.run(command, check=True, cwd='./web_crawler/web_crawler')


