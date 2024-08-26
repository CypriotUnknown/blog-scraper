import scrapy
from scrapy.http import HtmlResponse
from ..items import Article, ArticleMedia, ArticleAuthor
from utilities.get_categories_field import get_categories_fields
from ..blog_spider import BlogSpider


class StackLatestSpider(BlogSpider):
    name = "stack-latest"
    allowed_domains = ["stackoverflow.blog"]
    start_urls = ["https://stackoverflow.blog/"]

    def parse(self, response: HtmlResponse):
        yield from self.parseLatestArticles(response)
        yield from self.parseExternalArticles(response)

    def parseLatestArticles(self, response: HtmlResponse):
        articles = response.xpath(
            "//*[normalize-space(text())='Latest articles']/parent::div//article"
        )

        base_url = "https://stackoverflow.blog"

        for article in articles:
            date = article.xpath(".//time/@datetime").get()
            title = article.xpath(".//*[@itemprop='name']/text()").get()
            image = article.xpath(".//a/img/@src").get()
            url = article.xpath(".//img/parent::a/@href").get()
            url = f"{base_url}{url}" if url is not None else None

            description = article.xpath(".//*[@itemprop='abstract']/text()").get()
            author_name = article.xpath(".//a[@itemprop='author']/text()").get()
            author_url = article.xpath(".//a[@itemprop='author']/@href").get()
            author_url = f"{base_url}{author_url}" if author_url is not None else None

            author_image = article.xpath(
                ".//a[@itemprop='author']/parent::div/preceding-sibling::div/img/@src"
            ).get()

            categories = article.xpath(".//div[@itemprop='keywords']/a/text()").getall()

            yield Article(
                title=title,
                url=url,
                image=ArticleMedia(image),
                timestamp=date,
                description=description,
                author=ArticleAuthor(
                    name=author_name, url=author_url, icon_url=author_image
                ),
                fields=get_categories_fields(categories),
            )

    def parseExternalArticles(self, response: HtmlResponse):
        articles = response.xpath(
            "//div[normalize-space(text())='Around the web']/following-sibling::a"
        )

        for article in articles:
            url = article.xpath("./@href").get()
            title = article.xpath(".//h1/text()").get()
            description = article.xpath(".//p/text()").get()

            yield Article(title=title, url=url, description=description)
