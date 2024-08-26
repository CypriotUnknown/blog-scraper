import scrapy
from scrapy.http import HtmlResponse
from ..items import Article, ArticleMedia, ArticleFooter
from ..blog_spider import BlogSpider
from utilities import MOTORSPORTS_CATEGORY_CHANNEL


class F1LatestNewsSpider(BlogSpider):
    name = "f1-latest-news"
    allowed_domains = ["www.formula1.com"]
    start_urls = ["https://www.formula1.com/en/latest/all"]
    category_channel = MOTORSPORTS_CATEGORY_CHANNEL
    sort = True

    def parse(self, response: HtmlResponse):
        items = response.xpath(
            "//ul[substring(@aria-label, string-length(@aria-label) - string-length('articles') + 1) = 'articles']/li/a"
        )

        for item in items:
            url = item.xpath("@href").get()
            image = item.xpath(".//img/@src").get()
            category = item.xpath(".//figcaption/span/text()").get()
            title = item.xpath(".//figcaption/p/text()").get()

            article = Article(
                title=title,
                url=url,
                image=ArticleMedia(url=image),
                footer=ArticleFooter(text=category),
            )

            yield scrapy.Request(
                url=url, callback=self.parse_article_details, meta={"article": article}
            )

    def parse_article_details(self, response: HtmlResponse):
        article: Article = response.meta["article"]
        date = response.xpath("//time/@datetime").get()
        description = response.xpath(
            '//*[@id="maincontent"]/section[3]//p[1]//text()'
        ).get()

        article.timestamp = date
        article.description = description

        yield article
