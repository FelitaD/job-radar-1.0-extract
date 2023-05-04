import scrapy
from pathlib import Path

from scrapy.crawler import CrawlerProcess
from twisted.internet.error import DNSLookupError
from scrapy.loader import ItemLoader

from data_job_crawler.helpers.s3_helper import S3Helper
from data_job_crawler.crawler.items import OldJobsCrawlerItem

FILEPATH = Path(__file__).parent.parent / 'data' / 'unscanned_urls.txt'


class OldJobsSpider(scrapy.Spider):
    """
    Detects if a job position is still opened.
    Reads urls to be scanned from a text file and deletes them from the apply table.
    """

    name = "oldurls"

    def start_requests(self):
        links = S3Helper().extract_links_from_file(FILEPATH)
        for link in links:
            if 'datai.jobs' not in link:  # website is abandoned
                yield scrapy.Request(link,
                                     callback=self.parse_links,
                                     errback=self.parse_error,
                                     cb_kwargs=dict(main_url=link))

    def parse_links(self, response, main_url):
        l = ItemLoader(item=OldJobsCrawlerItem(), response=response)

        text_404 = response.xpath("//title[text()='Erreur 404']").get()
        text_pourvue = response.xpath('//*[text()="Cette offre a été pourvue !"]').get()

        if text_404 or text_pourvue:
            l.add_value('old_url', response.url)
            print('Sending for deletion', response.url)
            yield l.load_item()
        else:
            print('Keeping', response.url)

    def parse_error(self, failure):
        l = ItemLoader(item=OldJobsCrawlerItem(), response=failure)
        main_url = failure.request.cb_kwargs['main_url']

        if failure.value.response.status == 404:
            l.add_value('old_url', main_url)
            print('Sending for deletion', main_url)
            yield l.load_item()


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "ROBOTSTXT_OBEY": False,
            "ITEM_PIPELINES": {
                "data_job_crawler.crawler.pipelines.OldJobsCrawlerPipeline": 300,
            },
            "AUTOTHROTTLE_ENABLED": True,
            "AUTOTHROTTLE_TARGET_CONCURRENCY": 1,
            "AUTOTHROTTLE_START_DELAY": 5,
            "AUTOTHROTTLE_MAX_DELAY": 60,
        }
    )
    process.crawl(OldJobsSpider)
    process.start()
