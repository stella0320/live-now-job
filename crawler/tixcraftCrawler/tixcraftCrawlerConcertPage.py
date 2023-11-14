from multiprocessing import Process, Pool
import os, time
import requests
from bs4 import BeautifulSoup
from retry.api import retry_call
from time import process_time

class TixCraftCrawlerConcertPage():

    def __init__(self):
        self._concert_text_list=[]

    def request_url(self, url = None):
        web = requests.get(url, timeout=20)
        status = web.status_code
        print("子處理程序 ID: {}, 運送結果: {}, processTime:{}".format(os.getpid(), url, process_time()))
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
    
    def process_run(self, concert_url_list):
        t1_start = process_time()
        print('主處理程序 ID:', os.getpid())
        # cpus = os.cpu_count() 
        # print('cpuc:' + str(cpus))
        pool = Pool(4)
        result = pool.map(self.get_concert_info_html, concert_url_list)
        pool.close()
        pool.join()
        t1_stop = process_time()
        print("process:" + str(t1_stop-t1_start))
        return result

def process_pool():
    t1_start = process_time()
    print('主處理程序 ID:', os.getpid())
    # cpus = os.cpu_count() 
    # print('cpuc:' + str(cpus))
    pool = Pool(4)
    d = TixCraftCrawlerConcertPage()
    result = pool.map(d.get_concert_info_html, ['/activity/detail/24_rod', '/activity/detail/24_flybm', '/activity/detail/24_enhypen'])
    pool.close()
    pool.join()
    t1_stop = process_time()
    print(t1_stop-t1_start) 

def singleProcess():
    t1_start = process_time()
    url_list = ['/activity/detail/24_rod', '/activity/detail/24_flybm', '/activity/detail/24_enhypen']
    for url in url_list:
        d = TixCraftCrawlerConcertPage()
        d.get_concert_info_html(url)

    t1_stop = process_time()  
    print(t1_stop-t1_start)

if __name__ == '__main__':
    # singleProcess()
    process_pool()
    