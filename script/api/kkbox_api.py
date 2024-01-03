from requests.auth import HTTPBasicAuth
import requests
import os
from dotenv import load_dotenv
from retry.api import retry_call
import json
load_dotenv()


class KkboxApi():

    def get_token(self):
        url = 'https://account.kkbox.com/oauth2/token'
        input_param = {
            'grant_type': 'client_credentials',
            'client_id': os.getenv('KKBOX_CLIENT_ID'),
            'client_secret': os.getenv('KKBOX_SECRET')
        }

        result = requests.post(url=url, data=input_param)

        return result.json()

    def get_token_retry(self):
        result = retry_call(self.get_token, tries=3)
        return result

    def search_by_singer_name(self, singer_name):
        kkbox_api_token = self.get_token_retry()
        if kkbox_api_token:
            url = 'https://api.kkbox.com/v1.1/search'

            input_data = {
                'q': singer_name,
                'type': 'artist',
                'territory': 'TW',
                'offset': '0',
                'limit': '1'
            }

            authorization = 'Bearer {}'.format(
                kkbox_api_token.get('access_token'))
            header = {'Authorization': authorization,
                      'Accept': 'application/json'}

            result = requests.get(url=url, params=input_data, headers=header)
            result.encoding = 'utf-8'
        return result

    def search_by_singer_name_retry(self, singer_name):
        result = retry_call(self.search_by_singer_name, fkwargs={
                            "singer_name": singer_name}, tries=3)
        return result

    def search_image_url_by_singer_name_retry(self, singer_name):
        singer_info_result_kkbox = retry_call(self.search_by_singer_name, fkwargs={
            "singer_name": singer_name}, tries=3)

        singer_image_url = None
        if singer_info_result_kkbox.status_code == 200:
            singer_info_result = singer_info_result_kkbox.json()[
                'artists']['data']
            if singer_info_result:
                singer_info_result = singer_info_result[0]
                singer_image = singer_info_result.get('images')
                if singer_image:
                    singer_image_url = singer_image[1]['url']
        return singer_image_url
