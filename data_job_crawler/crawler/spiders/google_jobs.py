import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime

PROJECT_PATH = '/Users/donor/Library/Mobile Documents/com~apple~CloudDocs/PycharmProjects'


class GoogleJobsSpider(scrapy.Spider):
    """
    This Spider is used to render Javascript. It outputs all job links into a file.
    """

    name = "google_jobs"
    start_urls = [
        "https://www.google.com/search?q=junior+data+engineer+near+berlin&sxsrf=AB5stBggSW9RhZjrPXPBx8lHjw743l0wdg:1691177635227&source=hp&ei=o1LNZMaVC_WpkdUPqZqTuAM&iflsig=AD69kcEAAAAAZM1gswXevYg17W9dmNbxtgNf76QXxCA1&uact=5&oq=google+jobs+berlin&gs_lp=Egdnd3Mtd2l6IhJnb29nbGUgam9icyBiZXJsaW4yBRAAGIAEMgYQABgWGB4yCBAAGIoFGIYDSPMRUABY9Q9wAHgAkAEAmAGYAaAByAmqAQQxNS4yuAEDyAEA-AEBwgIHECMYigUYJ8ICBxAAGIoFGEPCAg0QLhiKBRjHARjRAxhDwgIEECMYJ8ICChAAGIAEGBQYhwLCAggQABiABBjLAcICCBAAGIoFGJECwgIHEAAYgAQYCg&sclient=gws-wiz&ibp=htl;jobs&sa=X&ved=2ahUKEwjE5ajT38OAAxUtSaQEHdcIAZQQutcGKAF6BAgaEBU#fpstate=tldetail&htivrt=jobs&htidocid=lxfgUDnPHmcAAAAAAAAAAA%3D%3D"
    ]

    links = set()

    # XPath to update when spider breaks (regularly)
    # Not best practice but website has dynamic attribute and aria roles
    # next_page_xpath = '//*[@aria-label="Pagination"]//li[last()]'
    job_links_xpath = '//*[@class="gws-plugins-horizon-jobs__tl-lif"]'

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            self.parse_jobs_list,
            meta={"playwright": True, "playwright_include_page": True},
        )

    async def parse_jobs_list(self, response):
        """Parse javascript rendered results page and obtain individual job page links."""
        page = response.meta["playwright_page"]

        # Accept google consent page
        await page.get_by_role("button", name="Tout accepter").click()

        # while True:
        #     try:
        #         job_elements = await page.query_selector_all(self.job_links_xpath)
        #
        #         for job_element in job_elements:
        #             job_link = await job_element.get_attribute("href")
        #             job_url = self.BASE_URL + job_link
        #             self.links.add(job_url)
        #
        #             ## For debugging
        #             # print('job_element', job_element)
        #             # print('job_link', job_link)
        #             # print('job_url', job_url)
        #             # print('links', self.links)
        #             print('\nScraped links count:', len(self.links), '\n')
        #
        #         next_locator = page.locator(self.next_page_xpath)
        #         async with page.expect_navigation():
        #             await next_locator.click()
        #
        #     except TimeoutError:
        #         print("Cannot find a next button on ", page.url)
        #         break
        #     finally:
        #         now = datetime.now().strftime('%d-%m-%y')
        #         with open(f'{PROJECT_PATH}/data-job-crawler/data_job_crawler/crawler/data'
        #                   f'/wttj_links_{now}.txt', "w+") as f:
        #             f.write(str(self.links))

        await page.close()


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "DOWNLOAD_HANDLERS": {
                "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
            "CONCURRENT_REQUESTS": 32,
            "ROBOTSTXT_OBEY": False,
            "AUTOTHROTTLE_ENABLED": True,
            "AUTOTHROTTLE_TARGET_CONCURRENCY": 1,
            "AUTOTHROTTLE_START_DELAY": 5,
            "AUTOTHROTTLE_MAX_DELAY": 60,
            "PLAYWRIGHT_LAUNCH_OPTIONS": {
                "headless": False,  # For debugging
                "timeout": 20 * 1000,  # 20 seconds
                "slow_mo": 10 * 1000  # slow down by 10 seconds to allow dynamic elements to load
            }
        }
    )
    process.crawl(GoogleJobsSpider)
    process.start()
