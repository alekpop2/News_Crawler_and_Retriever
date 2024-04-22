import scrapy

class ArticleSpider(scrapy.Spider):

    name = 'article_spider'
    allowed_domains = ['www.tmz.com']
    start_urls = ['https://www.tmz.com/', 'https://www.tmz.com/sports/', 'https://www.tmz.com/hip-hop/']
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'docs.csv',
    }

    def parse(self, response):
        
        article_headers = response.css('header.article__header')
        for header in article_headers:
            article_url = header.css('a').attrib['href']
            yield response.follow(article_url, callback = self.parse_articles)
        
        next_page_div = response.xpath("//div[@class='pagination--read-more mt-5']")
        if next_page_div:
            next_page_url = 'https://www.tmz.com' + next_page_div[-1].css('a').attrib['href']
            yield response.follow(next_page_url, callback = self.parse)
    
    def parse_articles(self, response):
        
        title_parts = response.css('h2.article__header-title').css('span::text').getall()
        title = ' '.join(title_parts)

        article_parts = response.xpath("//div[@class='article__blocks clearfix']").css('section')
        p_parts = list(filter(lambda part: part.xpath("./p"), article_parts))
        p_parts_lines = [part.css('::text').getall() for part in p_parts]
        p_texts = [' '.join(lines) for lines in p_parts_lines]
        all_text = ' '.join(p_texts)

        article_item = {
            'title' : title,
            'text' : all_text
        }
        
        yield article_item
