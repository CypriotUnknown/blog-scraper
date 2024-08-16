import scrapy
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings


class ScrapingBeeSpider(scrapy.Spider):
    name = "scrapingbee"
    allowed_domains = ["www.scrapingbee.com"]
    start_urls = ["https://www.scrapingbee.com/blog/"]

    custom_settings = {
        "ITEM_PIPELINES": {
            **get_project_settings().get("ITEM_PIPELINES", {}),
            "blog.pipelines.process_scrapingbee.ScrapingbeePipeline": 250,
        },
    }

    def parse(self, response: HtmlResponse):
        parent_divs = response.xpath('//a[starts-with(@href, "/blog/")]/parent::div')

        for div in parent_divs:
            time = div.css("time")

            if time.get() is None:
                yield None
            else:
                date = time.css("::text").get()
                image_url = div.css("img::attr(src)").get()
                title = div.css("img::attr(alt)").get()
                if len(title.strip()) == 0 or title is None:
                    title = div.css("h4::text").get()

                url = div.css("a::attr(href)").get()
                author_image = div.xpath(
                    '//img[starts-with(@src, "/images/authors/")]'
                ).attrib.get("src")
                author_name = div.css("strong::text").get()

                yield {
                    "url": url,
                    "title": title,
                    "image": image_url,
                    "date": date,
                    "author": {"image": author_image, "name": author_name},
                }
