import scrapy
from scrapy.http import HtmlResponse


class FreeCodecampSpider(scrapy.Spider):
    name = "free-codecamp"
    allowed_domains = ["www.freecodecamp.org"]
    start_urls = ["https://www.freecodecamp.org/news/"]

    def parse(self, response: HtmlResponse):
        articles = response.xpath(
            "//section[@class='post-feed']/article[@class='post-card']"
        )

        for article in articles:
            title = article.xpath(".//a/@aria-label").get()
            url = article.xpath(".//a/@href").get()
            image = article.xpath(".//img/@srcset").get()
            category_name = article.xpath(
                ".//span[@class='post-card-tags']/a/text()"
            ).get()
            category_url = article.xpath(
                ".//span[@class='post-card-tags']/a/@href"
            ).get()

            authors_list = article.xpath(".//ul[@class='author-list']/li")
            authors = []

            for author in authors_list:
                author_name = author.xpath(".//img/@alt").get()
                author_image = author.xpath(".//img/@src").get()
                author_url = author.xpath(".//a/@href").get()
                date = author.xpath(".//time/@datetime").get()

                authors.append(
                    {
                        "author_name": author_name,
                        "author_image": author_image,
                        "author_url": author_url,
                        "date": date,
                    }
                )

            yield {
                "title": title,
                "url": url,
                "image": image,
                "category": {"name": category_name, "url": category_url},
                "authors": authors,
            }
