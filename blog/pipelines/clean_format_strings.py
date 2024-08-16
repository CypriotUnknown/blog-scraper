def clean_and_format_string_values_in_dict(dictionary):
    if isinstance(dictionary, dict):
        for key, value in dictionary.items():
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
    def process_item(self, item, spider):
        item = clean_and_format_string_values_in_dict(item)
        return item
