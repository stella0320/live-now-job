from serviceTest.concert_info_service_test import ConcertInfoServiceTest
from serviceTest.singer_info_service_test import SingerInfoServiceTest
from serviceTest.concert_location_service_test import ConcertLocationServiceTest
from serviceTest.concert_time_table_service_test import ConcertTimeTableServiceTest

def concert_info_test():
    test_concert_info = ConcertInfoServiceTest()
    # test.test_update_column_values_by_id()
    data = test_concert_info.test_create_concert_info()
    print(data)


def singer_info_test():
    singer_info_serice_test = SingerInfoServiceTest()
    # singer_info_serice_test.test_create_singer_info()
    # singer_info_serice_test.test_find_singer_info_by_name()

    singer_info_serice_test.test_find_singer_info_by_name_or_create_new1()
    # singer_info_serice_test.test_find_singer_info_by_name_or_create_new2()

def concert_location_test():
    concert_location_service_test = ConcertLocationServiceTest()
    concert_location_service_test.test_find_concert_location_by_name_or_create_new()

def concert_time_table_test():
    test = ConcertTimeTableServiceTest()
    # test.test_creat_concert_time_list()
    test.test_delete_concert_time_table_by_concert_info_id()

if __name__ == '__main__':
   concert_info_test()
    

    

    