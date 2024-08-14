import json
import redis
import os


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
                        f"{channel_pattern}."
                        if channel_pattern[-1] != "."
                        else channel_pattern
                    )

                    self.redis_client = redis.Redis(
                        redis_host,
                        port=redis_port,
                        decode_responses=True,
                        username=file_json.get("username"),
                        password=file_json.get("password"),
                    )
                    self.items = []  # List to hold all scraped items

    def close_spider(self, spider):
        if self.redis_client is not None:
            items_json = json.dumps(self.items, indent=4)
            channel_name = self.channel_pattern + spider.name

            self.redis_client.publish(channel_name, items_json)
            print(f"published to Redis @ '{channel_name}'")

    def process_item(self, item, spider):
        # Add each item to the list
        if self.redis_client is not None:
            self.items.append(item)
        return item
