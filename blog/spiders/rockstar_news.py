from typing import Any
import scrapy
from scrapy.http import HtmlResponse
from ..items import Article, ArticleMedia, ArticleFooter


class RockstarNewsSpider(scrapy.Spider):
    name = "rockstar-news"
    allowed_domains = ["www.rockstargames.com"]
    start_urls = [
        r'https://graph.rockstargames.com/?origin=https://www.rockstargames.com&operationName=NewswireList&variables={"locale":"en_us","tagId":0,"page":1,"metaUrl":"/newswire"}&extensions={"persistedQuery":{"version":1,"sha256Hash":"eeb9e750157d583439e4858417291d5b09c07d7d48986858376a7a5a5d2f8a82"}}'
    ]

    def __init__(self, name: str | None = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.category_channel = "games"
        self.date_format = "%m/%d/%y, %I:%M %p"

    def parse(self, response: HtmlResponse):
        json = response.json()
        base_url = "https://www.rockstargames.com"
        items = json["data"]["posts"]["results"]

        for item in items:
            url = base_url + item["url"]
            title = item["title"]
            timestamp = item["created"]
            primary_tags = item["primary_tags"]

            if isinstance(primary_tags, list) and len(primary_tags) > 0:
                category = primary_tags[0]["name"]

            image = item["preview_images_parsed"]["newswire_block"]["d16x9"]

            yield Article(
                title=title,
                url=url,
                timestamp=timestamp,
                image=ArticleMedia(image),
                footer=ArticleFooter(text=category),
            )
