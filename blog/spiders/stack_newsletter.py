import scrapy
from scrapy.http import HtmlResponse
from ..items import Article
from ..blog_spider import BlogSpider


class StackNewsletterSpider(BlogSpider):
    name = "stack-newsletter"
    allowed_domains = ["stackoverflow.blog"]
    start_urls = ["https://stackoverflow.blog/newsletter"]

    def parse(self, response: HtmlResponse):
        articles = response.xpath('//time[@itemprop="datePublished"]/parent::a')
        base_url = "https://stackoverflow.blog"

        for article in articles:
            url = article.css("::attr(href)").get()
            url = f"{base_url}{url}" if url is not None else None

            date = article.css("time::attr(datetime)").get()
            title = article.css("[class*='headline']::text").get()
            description = article.css("p[class*='body']::text").get()

            yield Article(title=title, url=url, timestamp=date, description=description)
