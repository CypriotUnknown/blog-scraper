import scrapy
from scrapy.http import HtmlResponse
from ..items import Article, ArticleMedia, ArticleAuthor
from utilities.get_categories_field import get_categories_fields
from ..blog_spider import BlogSpider


class StackCareerSpider(BlogSpider):
    name = "stack-career"
    allowed_domains = ["stackoverflow.blog"]
    start_urls = ["https://stackoverflow.blog/career-advice/"]

    def parse(self, response: HtmlResponse):
        base_url = "https://stackoverflow.blog"
        articles = response.xpath(
            "//*[normalize-space(text())='career advice']/parent::div//article"
        )

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
                timestamp=date,
                image=ArticleMedia(image),
                author=ArticleAuthor(author_name, author_image, author_url),
                description=description,
                fields=get_categories_fields(categories),
            )
