import requests
import os
from retry.api import retry_call
from bs4 import BeautifulSoup
from time import process_time
from multiprocessing import Pool
from functools import reduce 
from datetime import datetime

class IndievoxCrawlerAllPartner():
    


    def request_url(self, url = None):
        web = requests.get(url, timeout=20)
        status = web.status_code
        print("子處理程序 ID: {}, 運送結果: {}, processTime:{}".format(os.getpid(), url, process_time()))
        if status == 200:
            return web
    
        return None
    
    def get_page(self, partner_url):
        page = retry_call(self.request_url, fkwargs={"url": partner_url}, tries=3)
        page_soup = BeautifulSoup(page.text, "html5lib")
        return page_soup

    # muti_process
    def run_partner_page(self, partner_page_url_list):
        t1_start = process_time()
        print('主處理程序 ID:', os.getpid())
        pool = Pool(4)
        result = pool.map(self.get_page, partner_page_url_list)
        pool.close()
        pool.join()
        t1_stop = process_time()
        print(t1_stop-t1_start)
        return result

    def handle_concert_time_table(self, concert_item, url):
        page = self.get_page(url)
        tr_list = page.select_one('#gameList').select('tr')
        concert_time_list = []
        concert_location = None
        for tr in tr_list:
            td_list = tr.select('td')
            for i in range(len(td_list)):
                if i==0:
                    time = td_list[0].get_text()
                    try:
                        if time:
                            time = time.replace('(日)', 'Sunday').replace('(六)', 'Saturday').replace('(五)', 'Friday').replace('(四)', 'Thursday').replace('(三)', 'Wednesday').replace('(二)', 'Tuesday').replace('(一)', 'Monday')
                            new_time = datetime.strptime(time, "%Y/%m/%d %A %H:%M")
                            format_time = new_time.strftime("%Y-%m-%d %H:%M")
                            concert_time_list.append(format_time)
                    except Exception as e:
                        print(e)
                if i==2:
                    concert_location = td_list[2].get_text()

        if len(concert_time_list) > 0:
            concert_item['concert_time'] = concert_time_list
        
        if concert_location:
            concert_item['concert_location_name'] = concert_location


    def handleConcertData(self, activity_list):
        result = []
        for activity in activity_list:
            item = {}
            ## 售票連結
            activity_page_url = activity.select_one('a')['href']
            item['concert_info_page_url'] = activity_page_url

            ## 演唱會圖片連結
            img_url = activity.select_one('img')['src']
            item['concert_info_image_url'] = img_url

            ## 演唱會標題
            titleElement = activity.select('.multi_ellipsis')
            if titleElement:
                item['concert_info_name'] = titleElement[0].get_text()

            item['concert_info_ticket_system_id'] = 2
            result.append(item)
        
        return result
    
    def get_concert_info_html(self, concert_page_url):
        # 單一場演唱會的頁面
        concert_web = retry_call(self.request_url, fkwargs={"url": concert_page_url}, tries=3)
        concert_text = None
        if concert_web:
            concert_soup = BeautifulSoup(concert_web.text, "html5lib")
            activity = concert_soup.select('#intro')
            concert_text = activity[0].get_text()

        return concert_text

if __name__ == '__main__':
    t1 = process_time()
    indievoxCrawler = IndievoxCrawlerAllPartner()
    result = indievoxCrawler.handle_concert_time_table('https://www.indievox.com/activity/game/23_iv0261630')
    print(result)
    # # 場館總攬單一頁面
    # partner_url = 'https://www.indievox.com/partner'

    # # 場館總攬單一頁面soup
    # indievox_partner_soup = indievoxCrawler.get_page(partner_url)

    # # 場館總攬單一頁面的每個場館element
    # indievox_partner_element_list = indievox_partner_soup.select('.avatar-block')

    # # 場館總攬單一頁面的每個場館element的url
    # partner_page_url_list =[partner_page_element.select_one('a')['href'] for partner_page_element in indievox_partner_element_list]
            
    # # 平行讀取url，所有單一場館web的soup
    # one_partner_concert_soup_list = indievoxCrawler.run_partner_page(partner_page_url_list)
    
    # activity_list_of_list = [one_page_element_list.select('.activity') for one_page_element_list in one_partner_concert_soup_list]
    # activity_list = reduce(list.__add__, activity_list_of_list)
    # # 串出每個場館頁面資料
    # result = indievoxCrawler.handleConcertData(activity_list)
    # print(len(result))
    # t2 = process_time()
    # print(t2-t1)

