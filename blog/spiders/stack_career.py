import scrapy
from scrapy.http import HtmlResponse


class StackCareerSpider(scrapy.Spider):
    name = "stack-career"
    allowed_domains = ["stackoverflow.blog"]
    start_urls = ["https://stackoverflow.blog/career-advice/"]

    def parse(self, response: HtmlResponse):
        articles = response.xpath(
            "//*[normalize-space(text())='career advice']/parent::div//article"
        )

        for article in articles:
            date = article.xpath(".//time/@datetime").get()
            title = article.xpath(".//*[@itemprop='name']/text()").get()
            image = article.xpath(".//img/@src").get()
            url = article.xpath(".//img/parent::a/@href").get()
            description = article.xpath(".//*[@itemprop='abstract']/text()").get()
            author_name = article.xpath(".//a[@itemprop='author']/text()").get()
            author_url = article.xpath(".//a[@itemprop='author']/@href").get()
            author_image = article.xpath(
                ".//a[@itemprop='author']/parent::div/preceding-sibling::div/img/@src"
            ).get()

            categories = article.xpath(".//div[@itemprop='keywords']/a/text()").getall()

            yield {
                "date": date,
                "title": title,
                "url": url,
                "image": image,
                "description": description,
                "author": {
                    "name": author_name,
                    "url": author_url,
                    "image": author_image,
                },
                "categories": categories,
            }
