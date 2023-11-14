from crawler.tixcraftCrawler import TixCraftCrawler
from service.concert_info_service import ConcertInfoService
from util.aws.s3_upload_file_api import S3UploadFileApi
from service.concert_time_table_service import ConcertTimeTableService
from openai import OpenAI
import os
import json
from datetime import datetime
from time import process_time
from multiprocessing import Process, Pool

from service.singer_info_service import SingerInfoService
from service.concert_location_service import ConcertLocationService
# 爬蟲

# 存每個演唱會資料
def save_concert_info_data(concert_item):
    item_data = tixCraftCrawler.handle_one_concert_page(concert_item)
    
    db_service1 = ConcertInfoService()
    db_concert_list = db_service1.find_concert_info_by_name(item_data['concert_info_name'])
    
    # 演唱會清單先存DB
    if not db_concert_list:
        db_service2 = ConcertInfoService()
        db_service2.create_concert_info(item_data)
        db_service3 = ConcertInfoService()
        db_concert_list = db_service3.find_concert_info_by_name(item_data['concert_info_name'])
    else:
        concert_info_id = getattr(db_concert_list[0], 'concert_info_id')
        db_service4 = ConcertInfoService()
        db_service4.update_column_values_by_id(item_data, concert_info_id)

    if db_concert_list:
        concert_info_id = getattr(db_concert_list[0], 'concert_info_id')
        item_data['concert_info_id'] = concert_info_id

    return item_data


if __name__ == '__main__':
    print('-start-')
    tixCraftCrawler = TixCraftCrawler()
    all_concert_list = tixCraftCrawler.handle_tixcraft_all_concert()
    all_concert_json_data = [save_concert_info_data(concert) for concert in all_concert_list if concert]
    print(all_concert_json_data)