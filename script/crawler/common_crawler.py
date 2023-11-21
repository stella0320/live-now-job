import requests
from bs4 import BeautifulSoup
from time import process_time
from urllib.parse import urlencode
from retry.api import retry_call
import os


def request_url(url=None):
    web = requests.get(url, timeout=20)
    status = web.status_code
    print("子處理程序 ID: {}, 運送結果: {}, processTime:{}".format(
        os.getpid(), url, process_time()))
    if status == 200:
        return web
    else:
        # 使用代理伺服器request
        web = requests.get(
            url='https://proxy.scrapeops.io/v1/',
            params={
                'api_key': 'c32fcd1f-6c4f-4022-b37b-ebc280574496',
                'url': urlencode(url),
                'country': 'tw'
            },
        )
        if web.status_code == 200:
            return web
    return None


def get_page(partner_url):
    page = retry_call(request_url, fkwargs={"url": partner_url}, tries=3)
    if page:
        page_soup = BeautifulSoup(page.text, "html5lib")
        return page_soup

    return None
