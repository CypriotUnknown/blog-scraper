from typing import Any
import scrapy
from scrapy.http import HtmlResponse
from ..items import Article, ArticleMedia, ArticleAuthor, ArticleFooter


class GithubLatestSpider(scrapy.Spider):
    name = "github-latest"
    allowed_domains = ["github.blog"]
    start_urls = ["https://github.blog/latest/"]

    def __init__(self, name: str | None = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.date_format = "%Y-%m-%d"

    def parse(self, response: HtmlResponse):
        articles = response.css("article")
        for article in articles:
            image = article.css("img::attr(src)").get()
            category_name = article.css("a::text").get()
            category_url = article.css("a::attr(href)").get()
            title = article.css("a[class='Link--primary card__link']::text").get()
            url = article.css("a[class='Link--primary card__link']::attr(href)").get()
            description = article.css("p::text").get()
            author_name = article.css("footer a[rel=author]::text").get()
            author_url = article.css("footer a[rel=author]::attr(href)").get()
            date = article.css("footer time::attr(datetime)").get()

            yield Article(
                title,
                url,
                date,
                ArticleMedia(image),
                ArticleAuthor(author_name, url=author_url),
                description,
                footer=ArticleFooter(text=category_name),
            )
