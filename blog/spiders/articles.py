import scrapy
from scrapy.http import HtmlResponse


class ArticlesSpider(scrapy.Spider):
    name = "articles"
    allowed_domains = ["www.calhoun.io"]
    start_urls = ["https://www.calhoun.io/page/1/"]

    base_url = "https://www.calhoun.io/page/"
    current_page = 1

    custom_settings = {
        "FEEDS": {"articles.json": {"format": "json", "indent": 4, "overwrite": True}}
    }

    def parse(self, response: HtmlResponse):
        if response.status is not 200:
            return
        # page_not_found = response.xpath(
        #     '//h1[contains(normalize-space(text()), "can\'t find the booty ye be looking for.")]'
        # ).get()

        # if page_not_found is not None:
        #     return

        print(f"SCRAPING PAGE: {self.current_page}")

        articles = response.css("div.block.pt-6.pb-0")

        for article in articles:
            url = article.css("a::attr(href)").get()
            title_all_text = article.css("a ::text").getall()
            non_empty_titles = [
                title.strip() for title in title_all_text if title.strip()
            ]
            title = non_empty_titles[0] if non_empty_titles else None
            preview = article.css("p::text").get()
            yield {"url": url, "title": title, "preview": preview}

        self.current_page += 1
        yield scrapy.Request(f"{self.base_url}{self.current_page}", callback=self.parse)
