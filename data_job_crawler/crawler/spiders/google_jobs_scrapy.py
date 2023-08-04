import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from data_job_crawler.crawler.items import JobsCrawlerItem


from datetime import datetime

PROJECT_PATH = '/Users/donor/Library/Mobile Documents/com~apple~CloudDocs/PycharmProjects'


class GoogleJobsScrapy(scrapy.Spider):
    """
    This Spider is used to render Javascript. It outputs all job links into a file.
    """

    name = "google_jobs_scrapy"
    start_urls = [
        "https://www.google.com/search?q=junior+data+engineer+near+berlin&sxsrf=AB5stBggSW9RhZjrPXPBx8lHjw743l0wdg:1691177635227&source=hp&ei=o1LNZMaVC_WpkdUPqZqTuAM&iflsig=AD69kcEAAAAAZM1gswXevYg17W9dmNbxtgNf76QXxCA1&uact=5&oq=google+jobs+berlin&gs_lp=Egdnd3Mtd2l6IhJnb29nbGUgam9icyBiZXJsaW4yBRAAGIAEMgYQABgWGB4yCBAAGIoFGIYDSPMRUABY9Q9wAHgAkAEAmAGYAaAByAmqAQQxNS4yuAEDyAEA-AEBwgIHECMYigUYJ8ICBxAAGIoFGEPCAg0QLhiKBRjHARjRAxhDwgIEECMYJ8ICChAAGIAEGBQYhwLCAggQABiABBjLAcICCBAAGIoFGJECwgIHEAAYgAQYCg&sclient=gws-wiz&ibp=htl;jobs&sa=X&ved=2ahUKEwjE5ajT38OAAxUtSaQEHdcIAZQQutcGKAF6BAgaEBU#fpstate=tldetail&htivrt=jobs&htidocid=lxfgUDnPHmcAAAAAAAAAAA%3D%3D"
    ]

    links = set()

    job_links_xpath = '//*[@class="gws-plugins-horizon-jobs__tl-lif"]'

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            self.parse_jobs_list,
            meta={"playwright": True, "playwright_include_page": True},
        )

    def parse_jobs_list(self, response):
        l = ItemLoader(item=JobsCrawlerItem(), response=response)
        l.add_value(
            "url",
            response.xpath(self.job_links_xpath).get(),
        )
        print(response.url)

        yield l.load_item()


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "ROBOTSTXT_OBEY": False,
            # "ITEM_PIPELINES": {
            #     "data_job_crawler.crawler.pipelines.JobsCrawlerPipeline": 300,
            # },
            "AUTOTHROTTLE_ENABLED": True,
            "AUTOTHROTTLE_TARGET_CONCURRENCY": 1,
            "AUTOTHROTTLE_START_DELAY": 5,
            "AUTOTHROTTLE_MAX_DELAY": 60,
        }
    )
    process.crawl(GoogleJobsScrapy)
    process.start()
