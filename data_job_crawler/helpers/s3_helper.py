import ast
import boto3
from datetime import datetime, timedelta
from pathlib import Path


class S3Helper:
    """
    Uploads new links by comparing 2 files.
    """

    def __init__(self):
        self.today = datetime.now().strftime('%d-%m-%y')
        self.bucket = "crawler-job-links"
        self.today_filename = self.get_filename_today()
        self.yesterday_filename = self.get_filename_yesterday()
        self.today_filepath = self.get_today_filepath()

    def upload_new_links(self):
        # Download latest file from S3
        yesterday_links = self.extract_links_from_s3('yesterday')

        # Get local file that we wish to add to S3
        today_links = self.extract_links_from_file()

        # Substracts from local file links already present on S3 file
        new_links = today_links - yesterday_links

        # Overwrite today's file with only new links
        with open(self.today_filepath, 'w') as f:
            f.write(str(new_links))

        self.upload_to_s3()

    def extract_links_from_file(self):
        with open(self.today_filepath, 'r') as f:
            links = f.read()
        return ast.literal_eval(links)

    def extract_links_from_s3(self, date='today'):
        s3 = boto3.resource('s3')
        dated_filename = ''
        if date == 'today':
            dated_filename = self.today_filename
        elif date == 'yesterday':
            dated_filename = self.yesterday_filename

        obj = s3.Object(self.bucket, key=dated_filename)
        links = obj.get()['Body'].read().decode('utf-8')
        return ast.literal_eval(links)

    def upload_to_s3(self):
        s3 = boto3.resource('s3')
        s3.Bucket(self.bucket).upload_file(self.today_filepath, self.today_filename)

    def get_filename_today(self):
        return f'wttj_links_{self.today}.txt'

    def get_filename_yesterday(self):
        yesterday = (datetime.today() - timedelta(days=1)).strftime('%d-%m-%y')
        return f'wttj_links_{yesterday}.txt'

    def get_today_filepath(self):
        return Path(__file__).parent.parent / 'crawler' / 'data' / self.today_filename


if __name__ == '__main__':
    S3Helper().upload_new_links()
