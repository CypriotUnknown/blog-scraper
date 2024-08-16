import scrapy
from datetime import datetime, timezone

import scrapy.exceptions


class ScrapingbeePipeline:
    base_url = "https://www.scrapingbee.com"

    def process_item(self, item: dict, spider: scrapy.Spider):
        item_url = item.get("url")

        if item_url is None:
            raise scrapy.exceptions.DropItem(item)

        item["url"] = self.base_url + item_url
        item_image = item.get("image")

        if item_image is not None:
            item["image"] = self.base_url + item_image

        item_title = item.get("title")

        if item_title is not None:
            item["title"] = item_title.lower()

        try:
            date_object = datetime.strptime(item.get("date"), "%d %B %Y")
            tz_offset = datetime.now(timezone.utc).astimezone().utcoffset()
            item["date"] = date_object.replace(tzinfo=timezone(tz_offset)).isoformat()
        except:
            pass

        author_name = item.get("author", {}).get("name")
        author_image = item.get("author", {}).get("image")

        if author_image is not None:
            item["author"]["image"] = self.base_url + item.get("author").get("image")

        if author_name is not None:
            item["author"]["name"] = author_name.lower()

        return item
