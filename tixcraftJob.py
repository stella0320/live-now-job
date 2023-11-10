from crawler.tixcraftCrawler import TixCraftCrawler
from service.concert_info_service import ConcertInfoService
from util.aws.s3_upload_file_api import S3UploadFileApi
from openai import OpenAI
import os
import json
# 爬蟲

tixCraftCrawler = TixCraftCrawler()

def save_concert_info_data(concert_item):
    item_data = tixCraftCrawler.handle_one_concert_page(concert_item)
    
    db_service = ConcertInfoService()
    db_concert_list = db_service.find_concert_info_by_name(item_data['concert_info_name'])
    
    # 演唱會清單先存DB
    if not db_concert_list:
        db_service = ConcertInfoService()
        db_service.create_concert_info(item_data)

        db_service = ConcertInfoService()
        db_concert_list = db_service.find_concert_info_by_name(item_data['concert_info_name'])
    else:
        
        concert_info_id = getattr(db_concert_list[0], 'concert_info_id')
        db_service = ConcertInfoService()
        db_service.update_column_values_by_id(item_data, concert_info_id)

    if db_concert_list:
        concert_info_id = getattr(db_concert_list[0], 'concert_info_id')
        item_data['concert_info_id'] = concert_info_id

    return item_data

def check_s3_content_same(item_data):
    #  cloudFront 確認文本重複
    concert_page_url = item_data['concert_info_page_url']
    concert_page_content = tixCraftCrawler.get_concert_info_html(concert_page_url)
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

def transfer_json_data_by_chat_gpt(concert_content):
    if concert_content:
        client = OpenAI(
            api_key=os.getenv('OPEN_AI_KEY'),
        )

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "You will be provided with unstructured chinese html text, and your task is to parse it into json format like this {'concert_time': list of YYYY-MM-E hh:mm, 'sell_ticket_time': list of  YYYY-MM-EE hh:mm, concert_singer: list of string ,concert_location:string}."},
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



########################main##################################
concert_list = tixCraftCrawler.handle_tixcraft_all_concert()
result = []
if concert_list:
    for concert_item in concert_list[4:6]:
        try:
            print('=========存資料開始========')
            item_data = save_concert_info_data(concert_item)

            print('=========存資料結束========')
            # 和S3上的文本比對內容是否一致
            check_s3_result = check_s3_content_same(item_data)
            
            if not check_s3_result['check_result']:
                print(f'concert_info_id:{item_data["concert_info_id"]}')
                # 如果文本沒有重複，跑chatgpt
                print('=========比對S3結束========')
                concert_json_data = transfer_json_data_by_chat_gpt(check_s3_result['concert_content'])
                print(concert_json_data)
                print('=========chatgpt結束========')

                item_data['concert_time'] = concert_json_data['concert_time']
                item_data['sell_ticket_time'] = concert_json_data['sell_ticket_time']
                item_data['concert_singer_name'] = concert_json_data['concert_singer']
                item_data['concert_location_name'] = concert_json_data['concert_location']
                result.append(item_data)
        except AttributeError as e:
            print(f"Exception:{e}")
            continue

print(result)


#####處理資料#####











