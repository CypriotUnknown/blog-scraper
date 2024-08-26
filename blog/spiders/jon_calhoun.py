import scrapy
from scrapy.http import HtmlResponse
from ..items import Article
from ..blog_spider import BlogSpider


class JonCalhounSpider(BlogSpider):
    name = "jon"
    allowed_domains = ["www.calhoun.io"]
    start_urls = ["https://www.calhoun.io/page/1/"]

    base_url = "https://www.calhoun.io/page/"
    page_to_scrape = 1

    def parse(self, response: HtmlResponse):
        if response.status is not 200:
            return

        articles = response.css("div.block.pt-6.pb-0")

        for article in articles:
            url = article.css("a::attr(href)").get()
            title_all_text = article.css("a ::text").getall()
            non_empty_titles = [
                title.strip() for title in title_all_text if title.strip()
            ]
            title = non_empty_titles[0] if non_empty_titles else None
            description = article.css("p::text").get()
            yield Article(title, url, description=description)

        self.page_to_scrape += 1
        yield scrapy.Request(
            f"{self.base_url}{self.page_to_scrape}", callback=self.parse
        )
