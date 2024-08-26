from scrapy.http import HtmlResponse
from ..items import Article, ArticleMedia, ArticleFooter, ArticleAuthor
from ..blog_spider import BlogSpider
from utilities import MOTORSPORTS_CATEGORY_CHANNEL


class DirtfishNewsSpider(BlogSpider):
    name = "dirtfish-news"
    allowed_domains = ["dirtfish.com"]
    start_urls = ["https://dirtfish.com/rally/wrc/"]
    category_channel = MOTORSPORTS_CATEGORY_CHANNEL

    def parse(self, response: HtmlResponse):
        items = response.xpath("//div[@id='archive-grid']//article")

        for item in items:
            url = item.xpath(".//a/@href").get()
            title = item.xpath(".//a/@title").get()
            image = item.xpath(".//a/img/@nitro-lazy-src").get()
            category = item.xpath(".//div[@class='entry-category']/a/text()").get()
            description = item.xpath(".//div[@class='entry-info']//p/text()").get()
            author_url = item.xpath(".//a[@rel='author']/@href").get()
            author_name = item.xpath(".//a[@rel='author']/text()").get()
            timestamp = item.xpath(".//time/@datetime").get()

            yield Article(
                title=title,
                url=url,
                image=ArticleMedia(image),
                footer=ArticleFooter(text=category),
                author=ArticleAuthor(name=author_name, url=author_url),
                description=description,
                timestamp=timestamp,
            )
