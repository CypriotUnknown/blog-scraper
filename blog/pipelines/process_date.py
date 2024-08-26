import scrapy
from datetime import datetime, timezone
from ..items import Article
from ..blog_spider import BlogSpider


class ProcessDatePipeline:
    def process_item(self, item: Article, spider: scrapy.Spider):
        try:
            datetime.fromisoformat(item.timestamp)
        except:
            try:
                if item.timestamp.isdigit():
                    # Convert timestamp (milliseconds) to seconds
                    timestamp_ms = int(item.timestamp)
                    timestamp_s = timestamp_ms / 1000.0
                    # Create a datetime object from the timestamp
                    dt = datetime.fromtimestamp(timestamp_s, tz=timezone.utc)
                    item.timestamp = dt.isoformat()
                else:
                    date_format = spider.date_format
                    date_object = datetime.strptime(item.timestamp, date_format)
                    tz_offset = datetime.now(timezone.utc).astimezone().utcoffset()
                    item.timestamp = date_object.replace(
                        tzinfo=timezone(tz_offset)
                    ).isoformat()
            except:
                item.timestamp = None

        return item
