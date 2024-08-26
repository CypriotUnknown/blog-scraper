from typing import Any, Optional
import scrapy
from scrapy.utils.project import get_project_settings
from scrapy import Spider


class BlogSpider(scrapy.Spider):
    category_channel: Optional[str] = None
    redis_pipeline_active: bool = True
    sort: bool = False

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BlogSpider, cls).from_crawler(crawler, *args, **kwargs)
        if not spider.redis_pipeline_active:
            print("Here !")
            # self.__remove_redis_pipeline()
            global_pipelines = get_project_settings().get("ITEM_PIPELINES", {})
            # Remove the specific pipeline
            spider.custom_settings = {
                # **self.custom_settings,
                "ITEM_PIPELINES": {
                    k: v
                    for k, v in global_pipelines.items()
                    if k != "blog.pipelines.redis_publish.RedisPublishPipeline"
                },
            }
        return spider

    def __remove_redis_pipeline(self):
        # Load existing pipelines from settings

        global_pipelines = get_project_settings().get("ITEM_PIPELINES", {})
        # Remove the specific pipeline
        self.custom_settings = {
            # **self.custom_settings,
            "ITEM_PIPELINES": {
                k: v
                for k, v in global_pipelines.items()
                if k != "blog.pipelines.redis_publish.RedisPublishPipeline"
            },
        }
