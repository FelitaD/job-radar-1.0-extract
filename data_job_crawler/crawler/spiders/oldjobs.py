from sqlalchemy import create_engine
import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
from twisted.internet.error import DNSLookupError
from scrapy.loader import ItemLoader

from data_job_crawler.crawler.items import JobsCrawlerItem
from data_job_crawler.config.definitions import DB_STRING


class OldJobsSpider(scrapy.Spider):
    """
    Detects if a job position is still opened.
    Reads urls to be scanned from a text file and deletes them from the apply table.
    """

    name = "old_jobs"

    def start_requests(self):
        open_null_or_false = self.extract_open_null_or_false()
        for i in range(len(open_null_or_false)):
            job_id = open_null_or_false.loc[i, 'id']
            link = open_null_or_false.loc[i, 'url']
            yield scrapy.Request(link,
                                 callback=self.parse_links,
                                 errback=self.parse_error,
                                 cb_kwargs={'job_id': job_id, 'link': link})

    @staticmethod
    def extract_open_null_or_false():
        engine = create_engine(DB_STRING)
        query = """
            SELECT url, id
            FROM processed_jobs AS p
            JOIN apply AS a
            ON p.id = a.job_id
            WHERE a.open IS NULL
                OR a.open IS FALSE;
        """
        return pd.read_sql_query(query, engine)

    def parse_links(self, response, job_id, link):
        print('Parse Links: \n')
        print(response.cb_kwargs['job_id'])

        l = ItemLoader(item=JobsCrawlerItem(), response=response)

        text_404 = response.xpath("//title[text()='Erreur 404']").get()
        text_pourvue = response.xpath('//*[text()="Cette offre a été pourvue !"]').get()

        if text_404 or text_pourvue:
            # l.add_value('job_id', response.cb_kwargs['job_id'])
            # print('Job offer closed: ', job_id)
            yield l.load_item()
        else:
            print('Still open: ', response.url)

    def parse_error(self, failure, job_id):
        print('Parse Error: \n')
        # print(failure.request.cb_kwargs['job_id'])

        l = ItemLoader(item=JobsCrawlerItem(), response=failure)

        # if failure.value.response.status == 404:
            # l.add_value('job_id', failure.request.cb_kwargs['job_id'])
            # print('Job offer closed: ', job_id)
            # yield l.load_item()


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "ROBOTSTXT_OBEY": False,
            # "ITEM_PIPELINES": {
            #     "data_job_crawler.crawler.pipelines.OldJobsCrawlerPipeline": 300,
            # },
            "AUTOTHROTTLE_ENABLED": True,
            "AUTOTHROTTLE_TARGET_CONCURRENCY": 1,
            "AUTOTHROTTLE_START_DELAY": 5,
            "AUTOTHROTTLE_MAX_DELAY": 60,
        }
    )
    process.crawl(OldJobsSpider)
    process.start()
