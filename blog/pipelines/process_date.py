import scrapy
from datetime import datetime, timezone
from ..items import Article


class ProcessDatePipeline:
    def process_item(self, item: Article, spider):
        try:
            date_format = spider.date_format
            date_object = datetime.strptime(item.timestamp, date_format)
            tz_offset = datetime.now(timezone.utc).astimezone().utcoffset()
            item.timestamp = date_object.replace(tzinfo=timezone(tz_offset)).isoformat()
        except:
            item.timestamp = None

        return item
