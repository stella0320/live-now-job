from ..crawler.crawler_handle_data import CrawlerHandleData

import os
from retry.api import retry_call
from bs4 import BeautifulSoup
from time import process_time
from multiprocessing import Pool
from datetime import datetime
from ..crawler.common_crawler import request_url, get_page


class IndievoxCrawler():
    crawlerHandleData = None

    # 平行requests.get url

    def run_mutiple_page(self, partner_page_url_list):
        t1_start = process_time()
        print('主處理程序 ID:', os.getpid())
        pool = Pool(4)
        result = pool.map(get_page, partner_page_url_list)
        pool.close()
        pool.join()
        t1_stop = process_time()
        print(t1_stop-t1_start)
        return result

    def handle_concert_time_table(self, concert_item, url):
        page = get_page(url)
        tr_list = page.select_one('#gameList').select('tr')
        concert_time_list = []
        concert_location = None
        for tr in tr_list:
            td_list = tr.select('td')
            for i in range(len(td_list)):
                if i == 0:
                    time = td_list[0].get_text()
                    try:
                        if time:
                            time = time.replace('(日)', 'Sunday').replace('(六)', 'Saturday').replace('(五)', 'Friday').replace(
                                '(四)', 'Thursday').replace('(三)', 'Wednesday').replace('(二)', 'Tuesday').replace('(一)', 'Monday')
                            new_time = datetime.strptime(
                                time, "%Y/%m/%d %A %H:%M")
                            format_time = new_time.strftime("%Y-%m-%d %H:%M")
                            concert_time_list.append(format_time)
                    except Exception as e:
                        print(e)
                if i == 2:
                    concert_location = td_list[2].get_text()

        if len(concert_time_list) > 0:
            concert_item['concert_time'] = concert_time_list

        if concert_location:
            concert_item['concert_location_name'] = concert_location

    def handle_concert_page_to_data(self, activity_list):
        result = []
        for activity in activity_list:
            item = {}
            # 售票連結
            activity_page_url = activity.select_one('a')['href']
            item['concert_info_page_url'] = activity_page_url

            # 演唱會圖片連結
            img_url = activity.select_one('img')['src']
            item['concert_info_image_url'] = img_url

            # 演唱會標題
            titleElement = activity.select('.multi_ellipsis')
            if titleElement:
                item['concert_info_name'] = titleElement[0].get_text()

            item['concert_info_ticket_system_id'] = 2
            result.append(item)

        return result

    def get_concert_info_html(self, concert_page_url):
        # 單一場演唱會的頁面
        concert_web = retry_call(request_url, fkwargs={
                                 "url": concert_page_url}, tries=3)
        concert_text = None
        if concert_web:
            concert_soup = BeautifulSoup(concert_web.text, "html5lib")
            activity = concert_soup.select('#intro')
            concert_text = activity[0].get_text()

        return concert_text

    # 找出所有場館的url
    def get_partner_pages(self):
        # 場館總攬頁面
        partner_url = 'https://www.indievox.com/partner'

        # 場館總攬單一頁面soup
        indievox_partner_soup = get_page(partner_url)

        # 場館總攬單一頁面的每個場館element
        indievox_partner_element_list = indievox_partner_soup.select(
            '.avatar-block')

        # 場館總攬單一頁面的每個場館element的url
        partner_page_url_list = [partner_page_element.select_one(
            'a')['href'] for partner_page_element in indievox_partner_element_list]

        return partner_page_url_list

    def save_concert_data(self, concert_list):
        self.crawlerHandleData = CrawlerHandleData(concert_list)
        self.crawlerHandleData.save_concert_info_data()

    def compare_S3_and_transfer_data_by_chat_gpt(self):
        crawlerHandleData = self.crawlerHandleData
        result = []
        if crawlerHandleData:
            result = self.crawlerHandleData.compare_S3_and_transfer_data_by_chat_gpt(
                self.get_concert_info_html)

        return result

    def special_handle_concert_time_data(self, concert_data):
        print('special_handle_concert_time_data 子處理程序 ID:', os.getpid())
        concert_info_page_url = concert_data.get('concert_info_page_url', None)
        if concert_info_page_url:
            time_page_url = concert_info_page_url.replace('detail', 'game')
            self.handle_concert_time_table(
                concert_data, time_page_url)

        return concert_data

    def run_special_handle_concert_time_data(self, concert_list):
        print('special_handle_concert_time_data 主處理程序 ID:', os.getpid())
        pool = Pool(4)
        result = pool.map(self.special_handle_concert_time_data, concert_list)
        pool.close()
        pool.join()
        return result

    def save_concert_all_data(self, concert_data):
        self.crawlerHandleData.save_concert_all_data(concert_data)
