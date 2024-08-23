from ..spiders.dirtfish_news import DirtfishNewsSpider


class DirtfishPodcastsSpider(DirtfishNewsSpider):
    name = "dirtfish-podcasts"
    allowed_domains = ["dirtfish.com"]
    start_urls = ["https://dirtfish.com/content/podcast/"]
