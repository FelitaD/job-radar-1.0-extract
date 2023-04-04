from diagrams import Diagram, Edge
from diagrams.onprem.database import Postgresql
from diagrams.programming.language import Python
from diagrams.custom import Custom
from diagrams.elastic.beats import Filebeat
from diagrams.aws.storage import SimpleStorageServiceS3BucketWithObjects as S3


with Diagram(name='Ingestion Data Flow', outformat="jpg", show=False):
    # Web sources
    web = Custom('Dynamically loaded content web page', 'web.png')

    # Text files
    txt = Filebeat('txt')

    # S3 bucket
    s3 = S3('crawler-job-links')

    # Spiders with library used for crawling
    links_spider = Custom('Scrapy + Playwright', 'playwright.png')
    spider = Custom('Spider with Scrapy', 'scrapy.png')
    scrapy_pipeline = Custom('Scrapy pipeline', 'scrapy.png')

    # Database
    raw_db = Postgresql('raw_jobs')

    # Dependencies
    web << Edge(label='crawls') << links_spider >> txt >> s3 << Edge(label='reads from') << spider
    spider >> scrapy_pipeline >> Edge(label='writes to') >> raw_db
