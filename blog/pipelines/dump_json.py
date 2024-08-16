import json
import os


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.items: list[dict] = []

    def close_spider(self, spider):
        directory = os.path.join(os.path.abspath(""), "data")
        file_path = os.path.join(directory, f"{spider.name}.json")
        os.makedirs(directory, exist_ok=True)

        with open(file_path, "w") as file:
            file.write(json.dumps(self.items, indent=4))

    def process_item(self, item, spider):
        self.items.append(item)
        return item
