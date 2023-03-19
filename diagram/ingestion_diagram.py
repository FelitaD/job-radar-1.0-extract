from diagrams import Diagram, Edge
from diagrams.onprem.database import Postgresql
from diagrams.programming.language import Python
from diagrams.custom import Custom
from diagrams.elastic.beats import Filebeat


with Diagram(name='Ingestion pipeline', outformat="jpg", show=False):
    # Web sources
    web_wttj = Custom('wttj.com/jobs', './diagram/welcome-to-the-jungle-squarelogo-1602063832341.png')
    web_spotify = Custom('lifeatspotify.com/jobs', './diagram/Spotify_icon.png')

    # Text files
    wttj_txt = Filebeat('wttj_links.txt')
    spotify_txt = Filebeat('spotify_links.txt')

    # Spiders with library used for crawling
    wttj_links = Custom('WttjLinksSpider', './diagram/playwright.png')
    wttj = Custom('WttjSpider', './diagram/scrapy.png')
    spotify_links = Custom('SpotifyLinksSpider', './diagram/playwright.png')
    spotify = Custom('SpotifySpider', './diagram/scrapy.png')
    scrapy_pipeline = Custom('JobsCrawlerPipeline', './diagram/scrapy.png')

    # Database
    raw_db = Postgresql('raw_jobs')

    # Dependencies
    web_wttj << Edge(label='crawls') << wttj_links >> wttj_txt << Edge(label='reads from') << wttj
    web_spotify << Edge(label='crawls') << spotify_links >> spotify_txt << Edge(label='reads from') << spotify

    [wttj, spotify] >> scrapy_pipeline >> Edge(label='writes to') >> raw_db
