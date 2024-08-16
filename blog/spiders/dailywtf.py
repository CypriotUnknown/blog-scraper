import scrapy
from scrapy.http import HtmlResponse
from datetime import datetime
from urllib.parse import urlparse


class DailywtfSpider(scrapy.Spider):
    name = "dailywtf"
    allowed_domains = ["thedailywtf.com"]
    today = datetime.now()
    start_urls = [
        f"https://thedailywtf.com/series/{today.year}/{today.month}/feature-articles",
        f"https://thedailywtf.com/series/{today.year}/{today.month}/code-sod",
        f"https://thedailywtf.com/series/{today.year}/{today.month}/errord",
    ]

    def parse(self, response: HtmlResponse):
        category = urlparse(response.url).path.split("/")[-1]

        articles = response.xpath(
            "//div[@id='article-feed']/div[starts-with(@class, 'article')]/div[@class='article-content']"
        )

        for article in articles:
            url = article.xpath("./a/@href").get()
            title = article.xpath(
                ".//*[@itemprop='headline'][@class='title']/text()"
            ).get()
            author_name = article.xpath(
                ".//span[@class='author'][@itemprop='name']/text()"
            ).get()
            source = article.xpath(
                ".//span[@class='source'][@itemprop='articleSection']/text()"
            ).get()
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
            )

            yield {
                "url": url,
                "title": title,
                "author_name": author_name,
                "source": source,
                "date": date,
                "body": body,
                "category": category,
            }
