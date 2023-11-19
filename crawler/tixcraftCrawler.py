import requests
from bs4 import BeautifulSoup
from retry import retry
from retry.api import retry_call
# 拓元爬蟲
from multiprocessing import Process, Pool

class TixCraftCrawler():
    
    def __init__(self):
        pass

    def request_url(self, url = None):
        
        proxies = {
            'https': 'https://f89b-2402-7500-487-be10-e528-d2a5-9153-7815.ngrok-free.app/',
        }

        headers = {
            'Content-Type': 'text/html',
            'ngrok-skip-browser-warning': 'XXX',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
        }

        web = requests.get(
            url='https://proxy.scrapeops.io/v1/',
            params={
                'api_key': 'c32fcd1f-6c4f-4022-b37b-ebc280574496',
                'url': url, 
                'country': 'tw'
            },
        )

        # web = requests.get(url, timeout=50, headers = headers, proxies=proxies)
        status = web.status_code
        if status == 200:
            return web
        
        return None

    def get_concert_info_html(self, url):
        # 單一場演唱會的頁面
        tixcraft_domain_name = 'https://tixcraft.com'
        concert_page_url = tixcraft_domain_name + url
        concert_web = retry_call(self.request_url, fkwargs={"url": concert_page_url}, tries=3)
        concert_text = None
        if concert_web:
            concert_soup = BeautifulSoup(concert_web.text, "html5lib")
            activity = concert_soup.select('#intro')
            concert_text = activity[0].get_text()

        return concert_text

    def handle_one_concert_page(self, one_concert_page):
        item = {}
        a = one_concert_page.find('a')

        # 演唱會標題
        titleElement = a.select('.multi_ellipsis')
        if titleElement:
            item['concert_info_name'] = titleElement[0].get_text()

        # 售票連結
        href = a['href']
        item['concert_info_page_url'] = href

        # 演唱會圖片連結
        img_url = a.find('img')['src']
        item['concert_info_image_url'] = img_url
        
        item['concert_info_ticket_system_id'] = 1

        return item


    # 所有演唱會的清單
    def handle_tixcraft_all_concert(self):
        tixcraft_ticket_list_url = 'https://tixcraft.com/activity'

        web = retry_call(self.request_url, fkwargs={"url": tixcraft_ticket_list_url}, tries=3)
        ticket_list = None
        if web:
            soup = BeautifulSoup(web.text, "html5lib")
            # 演唱會Div清單
            ticket_list = soup.select('.thumbnails')

        return ticket_list
    

if __name__ == '__main__':

    response = requests.get(
        url='https://proxy.scrapeops.io/v1/',
        params={
            'api_key': 'c32fcd1f-6c4f-4022-b37b-ebc280574496',
            'url': 'https://tixcraft.com/activity', 
            'country': 'tw'
        },
    )

    print('Response Body: ', response.status_code)
    
    
    # ip = 'http://114.37.217.13:80'
    # proxies = {
    #     'https': ip,
    #     'http': ip
    # }

    # headers = {
    #     'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    #     'Accept-Encoding': 'gzip, deflate, br',
    #     'User-Agent': 'python-requests/2.26.0'
    # }
    # web = requests.get("https://tixcraft.com/", headers= headers, timeout=50)
    # status = web.status_code

    # print(status)















