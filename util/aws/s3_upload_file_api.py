
import boto3
import calendar
import time
from botocore.exceptions import ClientError
import random
from io import BytesIO
import requests
from retry import retry
from retry.api import retry_call

class S3UploadFileApi:
    
    def __init__(self):
        pass

    def request_url(self, url = None):
        web = requests.get(url, timeout=20)
        status = web.status_code
        if status == 200:
            return web
        
        return None

    def hello_s3(self):
        """
        Use the AWS SDK for Python (Boto3) to create an Amazon Simple Storage Service
        (Amazon S3) resource and list the buckets in your account.
        This example uses the default settings specified in your shared credentials
        and config files.
        """
        s3_resource = boto3.resource("s3")
        print("Hello, Amazon S3! Let's list your buckets:")
        for bucket in s3_resource.buckets.all():
            print(bucket.name)

    def upload_file(self, text_content, concert_id):
        s3_resource = boto3.client("s3")
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        fileName = 'live_now/concert_' + str(concert_id) + '.txt' # modify
        file_data = BytesIO(text_content.encode('utf-8')) 
        s3_resource.upload_fileobj(file_data, 'my-image-jc', fileName, ExtraArgs={ "ContentType": "text/html; charset=UTF-8"})
        return fileName
    
    def check_concert_content_same_from_cloud_front(self, new_concert_content, concert_id):
        url = 'https://d305hij1yblnjs.cloudfront.net/live_now/concert_' + str(concert_id) + '.txt'
        concert_content = retry_call(self.request_url, fkwargs={"url": url}, tries=3)
        if concert_content:
            concert_content.encoding = 'utf-8'
            return new_concert_content == concert_content.text

        return False

if __name__ == "__main__":
    s3 = S3UploadFileApi()
    text_content = "Hello, this is some text content testXXX."
    s3.upload_file(text_content, 1)



