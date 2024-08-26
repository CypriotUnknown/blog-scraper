import scrapy
from scrapy.http import HtmlResponse
from ..items import Article, ArticleAuthor
from ..blog_spider import BlogSpider


class CodingHorrorSpider(BlogSpider):
    name = "coding-horror"
    allowed_domains = ["blog.codinghorror.com"]
    start_urls = ["https://blog.codinghorror.com/"]
    date_format = "%Y-%m-%d"

    def parse(self, response: HtmlResponse):
        items: list[Article] = []
        articles = response.xpath("//main/article")

        for article in articles:
            date = article.xpath(".//time/@datetime").get()
            title = article.xpath(".//*[@class='post-title']/a/text()").get()
            url = article.xpath(".//*[@class='post-title']/a/@href").get()
            url = f"https://blog.codinghorror.com{url}" if url is not None else None

            preview = "".join(
                article.xpath(".//section[@class='post-content']/p/text()").getall()
            )

            items.append(Article(title, url, date, description=preview))

        yield scrapy.Request(
            "https://blog.codinghorror.com/about-me",
            callback=self.parse_author_page,
            meta={"items": items},
        )

    def parse_author_page(self, response: HtmlResponse):
        author_name = response.xpath(
            '//section/p/text()[contains(., "I\'m")]/following-sibling::a/text()'
        ).get()

        author_url = response.xpath(
            '//section/p/text()[contains(., "I\'m")]/following-sibling::a/@href'
        ).get()

        author_image = response.xpath("//img/@src").get()

        for item in response.meta["items"]:
            item.author = ArticleAuthor(author_name, author_image, author_url)

            yield item
