import re
import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


class CodingHorrorSpider(scrapy.Spider):
    name = "coding-horror"
    allowed_domains = ["blog.codinghorror.com"]
    start_urls = [
        "https://blog.codinghorror.com/about-me",
        "https://blog.codinghorror.com/",
    ]

    def parse(self, response: HtmlResponse):
        split = list(
            filter(
                lambda component: len(component) > 0,
                map(
                    lambda component: component.strip(),
                    urlparse(response.url).path.split("/"),
                ),
            )
        )

        if len(split) > 0 and split[0] == "about-me":
            author_url = response.xpath(
                '//section/p/text()[contains(., "I\'m")]/following-sibling::a/@href'
            ).get()

            author_name = response.xpath(
                '//section/p/text()[contains(., "I\'m")]/following-sibling::a/text()'
            ).get()
            author_image = response.xpath("//img/@src").get()

            yield {
                "url": author_url,
                "image": author_image,
                "name": author_name,
            }
        else:
            articles = response.xpath("//main/article")

            for article in articles:
                date = article.xpath(".//time/@datetime").get()
                title = article.xpath(".//*[@class='post-title']/a/text()").get()
                url = article.xpath(".//*[@class='post-title']/a/@href").get()
                preview = "".join(
                    article.xpath(".//section[@class='post-content']/p/text()").getall()
                )

                yield {
                    "date": date,
                    "title": title,
                    "url": url,
                    "preview": preview,
                }
