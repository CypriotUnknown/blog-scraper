from ..items import Article
from ..blog_spider import BlogSpider


def clean_and_format_string_values_in_dict(dictionary):
    if isinstance(dictionary, dict):
        for key, value in dictionary.items():
            if "url" in key:
                continue

            if key == "text":
                dictionary[key] = value.upper().strip()
                continue

            if isinstance(value, dict):
                clean_and_format_string_values_in_dict(value)
            elif isinstance(value, str):
                dictionary[key] = value.lower().strip()
            elif isinstance(value, list):
                dictionary[key] = [
                    item.lower().strip() if isinstance(item, str) else item
                    for item in value
                ]

    return dictionary


class FormatStringsPipeline:
    def process_item(self, item: Article, spider):
        fixedDict = clean_and_format_string_values_in_dict(item.to_dict())
        return Article(**fixedDict)
