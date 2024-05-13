import script.service_test.concert_info_service_test as concert_info_service_test
import script.service_test.singer_info_service_test as singer_info_service_test
import script.service_test.concert_location_service_test as concert_location_service_test
import script.service_test.concert_time_table_service_test as concert_time_table_service_test
import script.api.kkbox_api as kkbox_api
import difflib
import script.service.singer_info_service as singer_info_service
import os
from dotenv import load_dotenv
load_dotenv()
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')
# 定義 handler 輸出 sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# 設定輸出格式
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# handler 設定輸出格式
console.setFormatter(formatter)
# 加入 hander 到 root logger
logging.getLogger('').addHandler(console)
test_logger = logging.getLogger('test.app')

def concert_info_test():

    test_concert_info1 = concert_info_service_test.ConcertInfoServiceTest()
    # test_concert_info1.test_create_concert_info()
    # test_concert_info = concert_info_service_test.ConcertInfoServiceTest()
    # test_concert_info.test_update_column_values_by_id()
    data = test_concert_info1.test_find_concert_info_by_name()
    print(data)
    print('finish')


def singer_info_test():
    singer_info_serice_test = singer_info_service_test.SingerInfoServiceTest()
    # singer_info_serice_test.test_create_singer_info()
    # singer_info_serice_test.test_find_singer_info_by_name()

    # singer_info_serice_test.test_find_singer_info_by_name_or_create_new1()
    # singer_info_serice_test.test_find_singer_info_by_name_or_create_new2()
    singer_info_serice_test.test_update_all_singer_image()


def concert_location_test():
    concert_location_service = concert_location_service_test.ConcertLocationServiceTest()
    concert_location_service.test_find_concert_location_by_name_or_create_new()


def concert_time_table_test():
    test = concert_time_table_service_test.ConcertTimeTableServiceTest()
    test.test_creat_concert_time_list()
    # test.test_delete_concert_time_table_by_concert_info_id()


def kkbox_api_test():
    kkbox_api = kkbox_api.KkboxApi()
    singer_name = '徐佳瑩'
    result = kkbox_api.search_by_singer_name_retry(singer_name)
    if result.status_code == 200:

        data = result.json()['artists']['data']
        # print(data)
        result = None
        max_simiar_value = 0
        for row in data:
            name = row.get('name')
            matcher = difflib.SequenceMatcher(None, singer_name, name)
            similarity = matcher.ratio()
            new_data = {
                'name': name,
                'image_url': row.get('images')[1],
                'similar': similarity
            }

            print(new_data)
            if similarity > max_simiar_value:
                max_simiar_value = similarity
                result = new_data

        print(result)


if __name__ == '__main__':

    host = os.getenv('DB_HOST')
    test_logger.info(host)