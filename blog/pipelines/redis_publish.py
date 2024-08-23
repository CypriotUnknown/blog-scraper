import json
import redis
import os
from ..items import Article
from scrapy.exceptions import DropItem
from datetime import datetime


class RedisPublishPipeline:
    def open_spider(self, spider):
        # Initialize Redis connection
        self.redis_client = None

        config_file_path = os.getenv("CONFIG_PATH", "redis-conf.json")
        if os.path.exists(config_file_path):
            with open(config_file_path, "r") as file:
                file_json = json.load(file)
                redis_host = file_json.get("host")
                redis_port = file_json.get("port")
                channel_pattern = file_json.get("channel_pattern")

                if (
                    redis_host is not None
                    and redis_port is not None
                    and channel_pattern is not None
                ):
                    self.channel_pattern = (
                        channel_pattern
                        if channel_pattern[-1] != "."
                        else channel_pattern.removesuffix(".")
                    )

                    self.redis_client = redis.Redis(
                        redis_host,
                        port=redis_port,
                        decode_responses=True,
                        username=file_json.get("username"),
                        password=file_json.get("password"),
                    )
                    self.items: list[Article] = []  # List to hold all scraped items
                    self.notification_flag: str | None = None

    def close_spider(self, spider):
        if self.redis_client is not None:
            try:
                should_sort = spider.sort == True
            except:
                should_sort = False

            if should_sort:
                self.items.sort(
                    key=lambda item: (
                        datetime.fromisoformat(item.timestamp)
                        if item.timestamp
                        else datetime.min
                    ),
                    reverse=True,
                )

            items_as_dict_array = [item.to_dict() for item in self.items]

            dict_to_send = {
                "articles": items_as_dict_array,
                "notificationFlag": self.notification_flag,
            }

            items_json = json.dumps(dict_to_send, indent=4)
            category_channel = "blogs"

            try:
                category_channel = spider.category_channel
            except:
                pass

            channel_name = ".".join(
                [self.channel_pattern, spider.name, category_channel, "articles"]
            )

            self.redis_client.publish(channel_name, items_json)
            print(f"published to Redis @ '{channel_name}'")

    def process_item(self, item: Article | None, spider):
        if item is None:
            print("ITEM IS NULL")
            raise DropItem(item)

        if item.title is None:
            print("ITEM TITLE IS NULL")
            raise DropItem(item)

        self.notification_flag = (
            "lastArticleDate" if item.timestamp is not None else "lastArticleTitle"
        )

        # Add each item to the list
        if self.redis_client is not None:
            self.items.append(item)
        return item
