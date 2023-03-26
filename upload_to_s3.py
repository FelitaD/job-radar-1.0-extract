import boto3
from datetime import datetime

now = datetime.now().strftime('%d-%m-%y')

s3 = boto3.resource('s3')
BUCKET = "crawler-job-links"

s3.Bucket(BUCKET).upload_file(f"data_job_crawler/crawler/spiders/data/wttj_links_{now}.txt", f"wttj_links_{now}.txt")
