from scrapy.http import HtmlResponse
from ..items import Article, ArticleMedia
from ..blog_spider import BlogSpider
from utilities import MOTORSPORTS_CATEGORY_CHANNEL


class DirtfishVideosSpider(BlogSpider):
    name = "dirtfish-videos"
    allowed_domains = ["dirtfish.com"]
    start_urls = ["https://dirtfish.com/videos/"]
    category_channel = MOTORSPORTS_CATEGORY_CHANNEL

    def parse(self, response: HtmlResponse):
        items = response.xpath("//a[@class='yotu-video']")
        base_url = "https://dirtfish.com/videos/"

        for item in items:
            title = item.xpath("@data-title").get()
            url = item.xpath("@href").get()
            url = base_url + url if url is not None else None
            image = item.xpath(".//img/@nitro-lazy-src").get()

            yield Article(title=title, url=url, image=ArticleMedia(image))
