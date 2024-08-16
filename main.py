import argparse
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os


def main(spiders: list[str]):
    settings = get_project_settings()

    print(f"Starting to crawl spiders: '{spiders}'")

    process = CrawlerProcess(settings)
    for spider in spiders:
        process.crawl(spider)

    process.start()
    print(f"Finished crawling spiders: '{spiders}'")


if __name__ == "__main__":
    load_dotenv(os.getenv("ENV_FILE_PATH", None))

    parser = argparse.ArgumentParser("WRC Scraper", description="Run wrc spider")
    parser.add_argument("-s", "--spider", type=str, help="name of the spider")

    args = parser.parse_args()

    spiders = []

    if args.spider is None:
        spiders_raw = os.getenv("SPIDERS")

        if spiders_raw is None:
            raise Exception(
                "YOU MUST PROVIDE A SPIDER. EITHER ON THE COMMAND LINE '-s <spider>' OR VIA THE 'SPIDERS' ENVIRONMENT VARIABLE"
            )

        spiders = list(map(lambda var: var.strip(), spiders_raw.split(",")))

    else:
        spiders = [args.spider]

    main(spiders)
