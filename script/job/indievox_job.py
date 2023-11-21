
from ..crawler.crawler_handle_data import CrawlerHandleData
from ..crawler.indievox_crawler import IndievoxCrawler
from time import process_time
from functools import reduce
from multiprocessing import Pool
import os


class IndievoxJob():

    def run(self):
        t1 = process_time()
        indievoxCrawler = IndievoxCrawler()

        partner_page_url_list = indievoxCrawler.get_partner_pages()

        # 1. 平行讀取url，所有單一場館web的soup
        one_partner_concert_soup_list = indievoxCrawler.run_mutiple_page(
            partner_page_url_list)

        # 2. 每個場館頁面的活動的element
        activity_list_of_list = [one_page_element_list.select(
            '.activity') for one_page_element_list in one_partner_concert_soup_list]
        activity_list = reduce(list.__add__, activity_list_of_list)
        # 3. 串出活動頁面資料
        concert_list = indievoxCrawler.handle_concert_page_to_data(
            activity_list)
        print(len(concert_list))
        t2 = process_time()
        print(t2-t1)
        result = []
        if concert_list:
            # test_list = concert_list[:3]

            # 資料先存DB，得到concert_info_id
            indievoxCrawler.save_concert_data(concert_list)

            # 資料和S3不同，再經過chat gpt轉換
            new_concert_list = indievoxCrawler.compare_S3_and_transfer_data_by_chat_gpt()

            # indievox 開演時間可以再用爬蟲比較正確的時間
            result = indievoxCrawler.run_special_handle_concert_time_data(
                new_concert_list)
            print(len(result))

            ##### 處理資料#####
            if len(result) > 0:
                for data in result:
                    if data:
                        indievoxCrawler.save_concert_all_data(data)
