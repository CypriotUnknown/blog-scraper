from blog.items import ArticleField


def get_categories_fields(categories: list[str]):
    return [
        ArticleField(name="Categories", value=""),
        *[
            ArticleField(name="", value=f" - {category}", inline=False)
            for category in categories
        ],
    ]
