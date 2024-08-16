import scrapy
from scrapy.http import HtmlResponse


class StackNewsletterSpider(scrapy.Spider):
    name = "stack-newsletter"
    allowed_domains = ["stackoverflow.blog"]
    start_urls = ["https://stackoverflow.blog/newsletter"]

    def parse(self, response: HtmlResponse):
        articles = response.xpath('//time[@itemprop="datePublished"]/parent::a')

        for article in articles:
            url = article.css("::attr(href)").get()
            date = article.css("time::attr(datetime)").get()
            title = article.css("[class*='headline']::text").get()
            description = article.css("p[class*='body']::text").get()

            yield {
                "url": url,
                "date": date,
                "title": title,
                "description": description,
            }
