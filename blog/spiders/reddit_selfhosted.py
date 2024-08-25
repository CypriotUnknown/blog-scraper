from scrapy.http import HtmlResponse
from ..items import Article, ArticleMedia, ArticleAuthor
from ..blog_spider import BlogSpider


class RedditSelfhostedSpider(BlogSpider):
    name = "reddit-selfhosted"
    allowed_domains = ["www.reddit.com"]
    start_urls = ["https://www.reddit.com/r/selfhosted/"]
    category_channel = "reddit"

    def parse(self, response: HtmlResponse):
        articles = response.xpath("//shreddit-post")
        base_url = "https://www.reddit.com"

        for article in articles:
            title = article.xpath("@post-title").get()
            url = article.xpath("@content-href").get()
            timestamp = article.xpath(".//faceplate-timeago/@ts").get()
            image = article.xpath(
                ".//div[@slot='post-media-container']//img/@src"
            ).get()

            author_name = article.xpath(
                ".//span[@slot='authorName']//faceplate-tracker//text()"
            ).get()

            author_name = author_name.removeprefix("u/") if author_name else None

            author_url = article.xpath(
                ".//span[@slot='authorName']//faceplate-tracker/a/@href"
            ).get()

            author_url = f"{base_url}{author_url}" if author_url else None

            author_image = article.xpath(
                ".//span[@slot='authorName']//faceplate-img/@src"
            ).get()
            description = article.xpath(".//a[@slot='text-body']//p//text()").getall()

            description = "".join(description) if description else None

            yield Article(
                title=title,
                url=url,
                timestamp=timestamp,
                author=ArticleAuthor(
                    name=author_name, icon_url=author_image, url=author_url
                ),
                description=description,
                image=ArticleMedia(image) if image else None,
            )
