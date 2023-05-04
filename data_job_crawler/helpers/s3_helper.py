import re

import ast
import boto3
from datetime import datetime
from pathlib import Path
import logging


class S3Helper:
    """
    Uploads new links by comparing 2 files.
    """

    def __init__(self):
        self.today = datetime.now().strftime('%d-%m-%y')
        self.today_filename = self.get_filename_today()
        self.today_filepath = self.get_today_filepath()

    def upload_new_links(self):
        # Download links from latest file on S3
        latest_links = self.extract_links_from_s3('latest')

        # Get local file that we wish to add to S3
        today_links = self.extract_links_from_file()

        # Prepare urls for comparison
        today_links_constant = self.extract_constant_url(today_links)
        latest_links_constant = self.extract_constant_url(latest_links)

        # Compare
        new_links = today_links_constant - latest_links_constant

        # Overwrite today's file with only new links
        with open(self.today_filepath, 'w') as f:
            f.write(str(new_links))

        self.upload_to_s3()

    @staticmethod
    def extract_constant_url(urls):
        matches = [re.search(r'.*(?=\?q=)', url) for url in urls]
        new_urls = [match.group(0) for match in matches if match is not None]
        if len(new_urls) > 0:
            return set(new_urls)
        return set(urls)

    def extract_links_from_s3(self, date='today'):
        s3 = boto3.resource('s3')
        bucket_name = "crawler-job-links"
        if date == 'today':
            filename = self.today_filename
        elif date == 'latest':
            filename = self.get_latest_modified(s3, bucket_name)
        obj = s3.Object(bucket_name, key=filename)
        links = obj.get()['Body'].read().decode('utf-8')
        return ast.literal_eval(links)

    @staticmethod
    def get_latest_modified(s3, bucket_name):
        bucket = s3.Bucket(bucket_name)
        latest_file = None
        last_modified_date = datetime(2022, 9, 1).replace(tzinfo=None)
        todays_date = datetime.now().replace(hour=0, minute=0, second=0)
        for file in bucket.objects.all():
            file_date = file.last_modified.replace(tzinfo=None)
            if last_modified_date < file_date < todays_date:
                last_modified_date = file_date
                latest_file = file
        return latest_file.key

    def extract_links_from_file(self):
        with open(self.today_filepath, 'r') as f:
            links = f.read()
        return ast.literal_eval(links)

    def upload_to_s3(self):
        s3 = boto3.resource('s3')
        s3.Bucket("crawler-job-links").upload_file(self.today_filepath, self.today_filename)

    def get_filename_today(self):
        return f'wttj_links_{self.today}.txt'

    def get_today_filepath(self):
        return Path(__file__).parent.parent / 'crawler' / 'data' / self.today_filename


if __name__ == '__main__':
    S3Helper().upload_new_links()
