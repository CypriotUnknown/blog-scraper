import json
import os
from ..items import Article
from ..blog_spider import BlogSpider


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.items: list[Article] = []

    def close_spider(self, spider):
        directory = os.path.join(os.path.abspath(""), "data")
        file_path = os.path.join(directory, f"{spider.name}.json")
        os.makedirs(directory, exist_ok=True)

        with open(file_path, "w") as file:
            file.write(json.dumps([item.to_dict() for item in self.items], indent=4))

    def process_item(self, item, spider):
        self.items.append(item)
        return item
