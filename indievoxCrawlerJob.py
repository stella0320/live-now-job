from crawler.indievoxCrawler.indievoxCrawlerAllPartner import IndievoxCrawlerAllPartner
from crawlerHandleData import CrawlerHandleData

from service.singer_info_service import SingerInfoService
from time import process_time
from functools import reduce
from multiprocessing import Pool
import os

def compare_S3_and_transfer_data_by_chat_gpt(item_data):
    print(" 子處理程序 ID:{}, concert_id:{}".format(os.getpid(), item_data.get('concert_info_id')))
    indievoxCrawler = IndievoxCrawlerAllPartner()
    crawlerHandleData = CrawlerHandleData()
    return crawlerHandleData.compare_S3_and_transfer_data_by_chat_gpt(item_data, indievoxCrawler.get_concert_info_html)


def run_compare_S3_and_transfer_data_by_chat_gpt(concert_list):
    print('handle S3 & chat gpt 主處理程序 ID:', os.getpid())
    pool = Pool(1)
    result = pool.map(compare_S3_and_transfer_data_by_chat_gpt, concert_list)
    pool.close()
    pool.join()
    return result

def special_handle_concert_time_data(concert_data):
    print('special_handle_concert_time_data 子處理程序 ID:', os.getpid())
    concert_info_page_url = concert_data.get('concert_info_page_url', None)
    if concert_info_page_url:
        indievoxCrawler = IndievoxCrawlerAllPartner()
        time_page_url = concert_info_page_url.replace('detail', 'game')
        indievoxCrawler.handle_concert_time_table(concert_data, time_page_url)
    
    return concert_data

def run_special_handle_concert_time_data(concert_list):
    list = [data for data in concert_list if data]
    print('special_handle_concert_time_data 主處理程序 ID:', os.getpid())
    pool = Pool(4)
    result = pool.map(special_handle_concert_time_data, list)
    pool.close()
    pool.join()
    return result

if __name__ == '__main__':
    t1 = process_time()
    indievoxCrawler = IndievoxCrawlerAllPartner()

    # 場館總攬單一頁面
    partner_url = 'https://www.indievox.com/partner'

    # 場館總攬單一頁面soup
    indievox_partner_soup = indievoxCrawler.get_page(partner_url)

    # 場館總攬單一頁面的每個場館element
    indievox_partner_element_list = indievox_partner_soup.select('.avatar-block')

    # 場館總攬單一頁面的每個場館element的url
    partner_page_url_list =[partner_page_element.select_one('a')['href'] for partner_page_element in indievox_partner_element_list]
            
    # 平行讀取url，所有單一場館web的soup
    one_partner_concert_soup_list = indievoxCrawler.run_partner_page(partner_page_url_list)
    
    activity_list_of_list = [one_page_element_list.select('.activity') for one_page_element_list in one_partner_concert_soup_list]
    activity_list = reduce(list.__add__, activity_list_of_list)
    # 串出每個場館頁面資料
    concert_list = indievoxCrawler.handleConcertData(activity_list)
    print(len(concert_list))
    t2 = process_time()
    print(t2-t1)
    result = []
    if concert_list:
        # test_list = concert_list[:3]
        crawlerHandleData = CrawlerHandleData(concert_list)
        crawlerHandleData.save_concert_info_data()
        concert_item_list = crawlerHandleData.get_concert_list()
        list_S3_chat_gpt = [compare_S3_and_transfer_data_by_chat_gpt(item_data) for item_data in concert_item_list if item_data]
        result = run_special_handle_concert_time_data(list_S3_chat_gpt)
        print(len(result))
        
        # result = run_compare_S3_and_transfer_data_by_chat_gpt(crawlerHandleData.get_concert_list())
        #####處理資料#####
        if len(result) > 0:
            for data in result:
                if data:
                    crawlerHandleData.save_concert_all_data(data)
