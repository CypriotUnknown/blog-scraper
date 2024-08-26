from typing import Any
import scrapy
from scrapy.http import XmlResponse
from scrapy.utils.project import get_project_settings
from ..items import Article, ArticleMedia, ArticleAuthor, ArticleFooter
from ..blog_spider import BlogSpider


class ScrapflySpider(BlogSpider):
    name = "scrapfly"
    allowed_domains = ["scrapfly.io"]
    start_urls = ["https://scrapfly.io/blog/rss/"]

    namespaces = {
        "content": "http://purl.org/rss/1.0/modules/content/",
        "dc": "http://purl.org/dc/elements/1.1/",
        "media": "http://search.yahoo.com/mrss/",
    }

    def __init__(self, name: str | None = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.date_format = "%a, %d %b %Y %H:%M:%S %Z"

    def parse(self, response: XmlResponse):

        for item in response.xpath("//item"):
            yield Article(
                title=item.xpath("title/text()").get(),
                url=item.xpath("link/text()").get(),
                timestamp=item.xpath("pubDate/text()").get(),
                description=item.xpath("description/text()").get(),
                image=ArticleMedia(
                    item.xpath("media:content/@url", namespaces=self.namespaces).get()
                ),
                author=ArticleAuthor(
                    item.xpath("dc:creator/text()", namespaces=self.namespaces).get()
                ),
                footer=ArticleFooter(
                    text=",".join(item.xpath("category/text()").getall())
                ),
            )
