from typing import Optional
import scrapy
from scrapy.utils.project import get_project_settings


class BlogSpider(scrapy.Spider):
    category_channel: Optional[str] = None
    redis_pipeline_active: bool = True
    sort: bool = False

    custom_settings = {
        "ITEM_PIPELINES": (
            {
                k: v
                for k, v in get_project_settings().get("ITEM_PIPELINES", {}).items()
                if k != "blog.pipelines.redis_publish.RedisPublishPipeline"
            }
            if not redis_pipeline_active
            else {
                k: v
                for k, v in get_project_settings().get("ITEM_PIPELINES", {}).items()
            }
        )
    }
