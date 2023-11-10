import requests
from bs4 import BeautifulSoup
from retry import retry
from retry.api import retry_call
# 拓元爬蟲


class TixCraftCrawler():
    
    def __init__(self):
        pass

    def request_url(self, url = None):
        web = requests.get(url, timeout=20)
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
















