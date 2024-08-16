import scrapy
from datetime import datetime, timezone

from scrapy.exceptions import DropItem


class GithubLatestPipeline:
    def process_item(self, item: dict, spider: scrapy.Spider):
        item_url = item.get("url")

        if item_url is None:
            raise DropItem(item)

        item_title = item.get("title")

        if item_title is not None:
            item["title"] = item_title.lower()

        item_description = item.get("description")

        if item_description is not None:
            item["description"] = item_description.lower()

        try:
            date_object = datetime.strptime(item.get("date"), "%Y-%m-%d")
            tz_offset = datetime.now(timezone.utc).astimezone().utcoffset()
            item["date"] = date_object.replace(tzinfo=timezone(tz_offset)).isoformat()
        except:
            item["date"] = None

        item_category = item.get("category", {}).get("name")

        if item_category is not None:
            item["category"]["name"] = item_category.lower()

        item_author = item.get("author", {}).get("name")

        if item_author is not None:
            item["author"]["name"] = item_author.lower()

        return item
