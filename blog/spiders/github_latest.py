import scrapy
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings


class GithubLatestSpider(scrapy.Spider):
    name = "github-latest"
    allowed_domains = ["github.blog"]
    start_urls = ["https://github.blog/latest/"]

    custom_settings = {
        "ITEM_PIPELINES": {
            **get_project_settings().get("ITEM_PIPELINES", {}),
            "blog.pipelines.process_github.GithubLatestPipeline": 250,
        },
    }

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

            yield {
                "title": title,
                "url": url,
                "description": description,
                "date": date,
                "image": image,
                "category": {
                    "name": category_name,
                    "url": category_url,
                },
                "author": {
                    "name": author_name,
                    "url": author_url,
                },
            }
