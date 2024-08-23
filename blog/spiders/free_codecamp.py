import scrapy
from scrapy.http import HtmlResponse
from ..items import Article, ArticleMedia, ArticleAuthor, ArticleFooter
from scrapy.utils.project import get_project_settings

class FreeCodecampSpider(scrapy.Spider):
    name = "free-codecamp"
    allowed_domains = ["www.freecodecamp.org"]
    start_urls = ["https://www.freecodecamp.org/news/"]

    # Load existing pipelines from settings
    global_pipelines = get_project_settings().get('ITEM_PIPELINES', {})

    # Remove the specific pipeline
    custom_settings = {
        "ITEM_PIPELINES": {
            k: v for k, v in global_pipelines.items() if k != 'blog.pipelines.process_date.ProcessDatePipeline'
        }
    }

    def parse(self, response: HtmlResponse):
        articles = response.xpath(
            "//section[@class='post-feed']/article[@class='post-card']"
        )

        base_url = "https://www.freecodecamp.org"

        for article in articles:
            title = article.xpath(".//a/@aria-label").get()
            url = article.xpath(".//a/@href").get()
            image = article.xpath(".//img/@srcset").get()
            category_name = article.xpath(
                ".//span[@class='post-card-tags']/a/text()"
            ).get()
            # category_url = article.xpath(
            #     ".//span[@class='post-card-tags']/a/@href"
            # ).get()

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

            yield Article(
                title=title,
                url=f"{base_url}{url}" if url is not None else None,
                image=ArticleMedia(image),
                author=(
                    ArticleAuthor(
                        name=authors[0]["author_name"],
                        icon_url=authors[0]["author_image"],
                        url=f"{base_url}{authors[0]["author_url"]}" if authors[0]["author_url"] is not None else None,
                    )
                    if len(authors) > 0
                    else None
                ),
                footer=ArticleFooter(text=category_name),
                timestamp=authors[0]["date"] if len(authors) > 0 else None,
            )
