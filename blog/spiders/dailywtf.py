from typing import Any
import scrapy
from scrapy.http import HtmlResponse
from datetime import datetime
from urllib.parse import urlparse
from ..items import Article, ArticleAuthor, ArticleFooter
from ..blog_spider import BlogSpider


class DailywtfSpider(BlogSpider):
    name = "dailywtf"
    allowed_domains = ["thedailywtf.com"]
    today = datetime.now()
    start_urls = [
        f"https://thedailywtf.com/series/{today.year}/{today.month}/feature-articles",
        f"https://thedailywtf.com/series/{today.year}/{today.month}/code-sod",
        f"https://thedailywtf.com/series/{today.year}/{today.month}/errord",
    ]

    def __init__(self, name: str | None = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.date_format = "%Y-%m-%d"
        self.sort = True

    def parse(self, response: HtmlResponse):
        category = urlparse(response.url).path.split("/")[-1]

        articles = response.xpath(
            "//div[@id='article-feed']/div[starts-with(@class, 'article')]/div[@class='article-content']"
        )

        for article in articles:
            url = article.xpath("./a/@href").get()

            if url is not None:
                title = article.xpath(
                    ".//*[@itemprop='headline'][@class='title']/text()"
                ).get()
                # author_name = article.xpath(
                #     ".//span[@class='author'][@itemprop='name']/text()"
                # ).get()
                # source = article.xpath(
                #     ".//span[@class='source'][@itemprop='articleSection']/text()"
                # ).get()
                date = article.xpath(
                    ".//span[@class='date'][@itemprop='datePublished']/@content"
                ).get()
                body = "".join(
                    list(
                        filter(
                            lambda text: len(text) > 0,
                            article.xpath(
                                ".//div[@itemprop='articleBody']//text()"
                            ).getall(),
                        )
                    )
                ).strip()

                article = Article(
                    title=title,
                    url=url,
                    timestamp=date,
                    description=body,
                    footer=ArticleFooter(text=category),
                )

                yield scrapy.Request(
                    url=url, callback=self.parse_author, meta={"article": article}
                )
            else:
                yield None

    def parse_author(self, response: HtmlResponse):
        author_name = response.xpath(
            "//div[@itemprop='author']/a[@itemprop='name']/text()"
        ).get()
        author_image = response.xpath("//div[@itemprop='author']/img/@src").get()
        author_url = response.xpath(
            "//div[@itemprop='author']/a[@itemprop='name']/@href"
        ).get()

        base_url = "https://thedailywtf.com"
        if author_url is not None and author_url.strip().startswith("/"):
            author_url = f"{base_url}{author_url}"

        if author_image is not None and author_image.strip().startswith("/"):
            author_image = f"{base_url}{author_image}"

        article: Article = response.meta["article"]

        article.author = ArticleAuthor(
            name=author_name,
            icon_url=author_image,
            url=author_url,
        )

        yield article
