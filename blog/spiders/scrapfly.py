import scrapy
from scrapy.http import XmlResponse


class ScrapflySpider(scrapy.Spider):
    name = "scrapfly"
    allowed_domains = ["scrapfly.io"]
    start_urls = ["https://scrapfly.io/blog/rss/"]

    namespaces = {
        "content": "http://purl.org/rss/1.0/modules/content/",
        "dc": "http://purl.org/dc/elements/1.1/",
        "media": "http://search.yahoo.com/mrss/",
    }

    def parse(self, response: XmlResponse):
        # Loop through each item in the RSS feed
        for item in response.xpath("//item"):
            yield {
                "title": item.xpath("title/text()").get(),
                "link": item.xpath("link/text()").get(),
                "creator": item.xpath(
                    "dc:creator/text()", namespaces=self.namespaces
                ).get(),
                # "content": item.xpath(
                #     "content:encoded/text()", namespaces=self.namespaces
                # ).get(),
                "description": item.xpath("description/text()").get(),
                "pub_date": item.xpath("pubDate/text()").get(),
                "categories": item.xpath("category/text()").getall(),
                "images": item.xpath(
                    "media:content/@url", namespaces=self.namespaces
                ).get(),
            }
