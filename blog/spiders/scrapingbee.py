from scrapy.http import HtmlResponse
from ..items import Article, ArticleMedia, ArticleAuthor
from ..blog_spider import BlogSpider


class ScrapingBeeSpider(BlogSpider):
    name = "scrapingbee"
    allowed_domains = ["www.scrapingbee.com"]
    start_urls = ["https://www.scrapingbee.com/blog/"]

    def parse(self, response: HtmlResponse):
        parent_divs = response.xpath('//a[starts-with(@href, "/blog/")]/parent::div')
        base_url = "https://www.scrapingbee.com"

        for div in parent_divs:
            time = div.css("time")

            if time.get() is None:
                yield None
            else:
                date = time.css("::text").get()
                image_url = div.css("img::attr(src)").get()
                image_url = f"{base_url}{image_url}" if image_url is not None else None

                title = div.css("img::attr(alt)").get()
                if len(title.strip()) == 0 or title is None:
                    title = div.css("h4::text").get()

                url = div.css("a::attr(href)").get()
                url = f"{base_url}{url}" if url is not None else None

                author_image = div.xpath(
                    '//img[starts-with(@src, "/images/authors/")]'
                ).attrib.get("src")
                author_image = (
                    f"{base_url}{author_image}" if author_image is not None else None
                )

                author_name = div.css("strong::text").get()

                yield Article(
                    title,
                    url,
                    date,
                    ArticleMedia(image_url),
                    ArticleAuthor(author_name, author_image),
                )
