from service.concert_info_service import ConcertInfoService
from service.singer_info_service import SingerInfoService
from service.concert_location_service import ConcertLocationService
from service.concert_time_table_service import ConcertTimeTableService
from util.aws.s3_upload_file_api import S3UploadFileApi
from openai import OpenAI
import os
import json
from datetime import datetime


class CrawlerHandleData():
    
    def __init__(self, concert_list = []):
        self.__concert_list = concert_list
    
    def get_concert_list(self):
        return self.__concert_list

    def save_concert_info_data(self):
    
        concert_ite_list  = self.__concert_list

        for concert_item in concert_ite_list:
            
            db_service1 = ConcertInfoService()
            db_concert_list = db_service1.find_concert_info_by_name(concert_item['concert_info_name'])
            
            # 演唱會清單先存DB
            if not db_concert_list:
                db_service2 = ConcertInfoService()
                db_service2.create_concert_info(concert_item)
                db_service3 = ConcertInfoService()
                db_concert_list = db_service3.find_concert_info_by_name(concert_item['concert_info_name'])
            else:
                concert_info_id = getattr(db_concert_list[0], 'concert_info_id')
                db_service4 = ConcertInfoService()
                db_service4.update_column_values_by_id(concert_item, concert_info_id)

            if db_concert_list:
                concert_info_id = getattr(db_concert_list[0], 'concert_info_id')
                concert_item['concert_info_id'] = concert_info_id

        return concert_item
    
    # S3 文本比對
    def check_s3_content_same(self, item_data, crawl_web_func):
        #  cloudFront 確認文本重複
        concert_page_url = item_data['concert_info_page_url']
        concert_page_content = crawl_web_func(concert_page_url)
        concert_info_id = item_data['concert_info_id']

        check_s3_same_with_new_conent = False
        if concert_page_content and concert_info_id:
            s3_upload_file_api = S3UploadFileApi()
            check_s3_same_with_new_conent = s3_upload_file_api.check_concert_content_same_from_cloud_front(concert_page_content, concert_info_id)

        print(f'concert_info_id:{concert_info_id}, check_s3_same_with_new_conent:{check_s3_same_with_new_conent}')

        # 如果文本沒有重複，上傳S3
        if not check_s3_same_with_new_conent and concert_page_content:
            s3_upload_file_api = S3UploadFileApi()
            s3_upload_file_api.upload_file(concert_page_content, concert_info_id)

        return {
            'check_result': check_s3_same_with_new_conent,
            'concert_content': concert_page_content
        }
    

    # Open AI API
    def transfer_json_data_by_chat_gpt(self, concert_content):
        if concert_content:
            client = OpenAI(
                api_key=os.getenv('OPEN_AI_KEY'),
            )

            completion = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=[
                    {"role": "system", "content": "You will be provided with unstructured chinese html text, and your task is to parse it into json format like this {'concert_time': list of YYYY-MM-E hh:mm, 'sell_ticket_time': list of  YYYY-MM-EE hh:mm, concert_singer_name: string ,concert_location:string}."},
                    {"role": "user", "content": concert_content}
                ],
                temperature=0,
                max_tokens=500
            )

            try:
                if completion:
                    response = completion.choices[0].message
                    if response:
                        result_chat_gpt_str = getattr(response, 'content')
                        result_chat_gpt_json = json.loads(result_chat_gpt_str)
                        return result_chat_gpt_json

            except Exception as e:
                print(str(e))
        return None
    
    def compare_S3_and_transfer_data_by_chat_gpt(self, item_data, crawl_web_func):
        try:
            
            print('=========存資料結束========')
            # 和S3上的文本比對內容是否一致
            check_s3_result = self.check_s3_content_same(item_data, crawl_web_func)
            
            if not check_s3_result['check_result']:
                print(f'concert_info_id:{item_data["concert_info_id"]}')
                # 如果文本沒有重複，跑chatgpt
                print('=========比對S3結束========')
                concert_json_data = self.transfer_json_data_by_chat_gpt(check_s3_result['concert_content'])
                print(concert_json_data)
                print('=========chatgpt結束========')

                item_data['concert_time'] = concert_json_data['concert_time']
                item_data['sell_ticket_time'] = concert_json_data['sell_ticket_time']
                item_data['concert_singer_name'] = concert_json_data['concert_singer_name']
                item_data['concert_location_name'] = concert_json_data['concert_location']
        except AttributeError as e:
            print(f"Exception:{e}")
        
        return item_data


    def handle_concert_time_data(self, time_data, concert_info_id, time_table_type):
        result = []
        for data in time_data:
            date_obj = datetime.strptime(data, '%Y-%m-%d %H:%M')
            item = {
                'concert_time_table_type':time_table_type,
                'concert_info_id':concert_info_id,
                'concert_time_table_datetime': date_obj
            }
            result.append(item)
        
        return result

    def save_concert_all_data(self, data):
        if data:

            # concert singer update
            singer_info_service = SingerInfoService()
            signer_id = singer_info_service.find_singer_info_by_name_or_create_new(data['concert_singer_name'])

            # concert location update
            concert_location_service = ConcertLocationService()
            concert_location_id = concert_location_service.find_concert_location_by_name_or_create_new(data['concert_location_name'])

            # update concert info
            concert_info_id = data['concert_info_id']

            concert_info_service = ConcertInfoService()
            concert_info_update_data = {
                'concert_info_location_id': concert_location_id,
                'concert_info_singer_id':signer_id
            }
            concert_info_service.update_column_values_by_id(concert_info_update_data, concert_info_id)

            

            # concert_time_table
            concert_time = data['concert_time']
            sell_ticket_time = data['sell_ticket_time']

            concert_time_table_service = ConcertTimeTableService()
            concert_time_table_service.delete_concert_time_table_by_concert_info_id(concert_info_id)

            if concert_time and len(concert_time) > 0:
                concert_time_list = self.handle_concert_time_data(concert_time, concert_info_id, '演出時間')
                concert_time_table_service_for_concert_time = ConcertTimeTableService()
                concert_time_table_service_for_concert_time.creat_concert_time_list(concert_time_list)

            if sell_ticket_time and len(sell_ticket_time) > 0:
                sell_ticket_time_list = self.handle_concert_time_data(sell_ticket_time, concert_info_id, '售票時間')
                concert_time_table_service_for_sell_ticket_time = ConcertTimeTableService()
                concert_time_table_service_for_sell_ticket_time.creat_concert_time_list(sell_ticket_time_list)


