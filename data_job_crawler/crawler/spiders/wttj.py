import scrapy
import re
from datetime import datetime

from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from itemloaders.processors import Join

from data_job_crawler.helpers.s3_helper import S3Helper
from data_job_crawler.crawler.items import JobsCrawlerItem


class WttjSpider(scrapy.Spider):
    """
    Spider to scrape jobs information on Welcome to the Jungle Website.
    The individual pages are not rendered with Javascript so it only uses Scrapy.
    """

    name = "wttj"

    def start_requests(self):
        helper = S3Helper()
        links = helper.extract_links_from_s3('today')
        for link in links:
            yield scrapy.Request(link, self.yield_job_item)

    def yield_job_item(self, response):
        l = ItemLoader(item=JobsCrawlerItem(), response=response)

        match = re.search(r'.*(?=\?q=)', response.url)  # url with random ending
        if match:
            l.add_value("url", match.group(0))
        else:
            l.add_value("url", response.url)

        l.add_value(
            "title",
            response.xpath(
                '//a[@data-testid="job-header-organization-link-logo"]/parent::div/h1/text()[2]'
            ).get(),
        )
        l.add_value(
            "company",
            response.xpath(
                '//a[@data-testid="job-header-organization-link-logo"]/parent::div/a/span/text()'
            ).get(),
        )
        l.add_value(
            "location",
            response.xpath(
                '//*[@name="location"]/parent::span/following-sibling::span//text()'
            ).get(),
        )
        l.add_value(
            "type",
            response.xpath(
                '//i[@name="contract"]/following-sibling::span/text()'
            ).get(),
        )
        l.add_value(
            "industry",
            response.xpath(
                '//*[@name="tag"]/parent::span/following-sibling::span/text()'
            ).get(),
        )
        l.add_value('size', response.xpath('//*[@name="department"]/parent::span/following-sibling::span/text()').get())
        l.add_value('experience', response.xpath('//i[@name="suitcase"]/following-sibling::span/text()').get())
        l.add_value('education', response.xpath('//i[@name="education_level"]/following-sibling::span/text()').get())
        l.add_value(
            "text",
            response.xpath("//h2/following-sibling::div//text()").getall(),
            Join(),
        )
        l.add_value(
            "remote",
            response.xpath(
                '//i[@name="remote"]/following-sibling::span/text()'
            ).get(),
        )
        l.add_value("created_at", datetime.now())

        yield l.load_item()


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "ROBOTSTXT_OBEY": False,
            "ITEM_PIPELINES": {
                "data_job_crawler.crawler.pipelines.JobsCrawlerPipeline": 300,
            },
            "AUTOTHROTTLE_ENABLED": True,
            "AUTOTHROTTLE_TARGET_CONCURRENCY": 1,
            "AUTOTHROTTLE_START_DELAY": 5,
            "AUTOTHROTTLE_MAX_DELAY": 60,
        }
    )
    process.crawl(WttjSpider)
    process.start()
