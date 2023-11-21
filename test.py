import script.service_test.concert_info_service_test as concert_info_service_test
import script.service_test.singer_info_service_test as singer_info_service_test
import script.service_test.concert_location_service_test as concert_location_service_test
import script.service_test.concert_time_table_service_test as concert_time_table_service_test


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


def concert_location_test():
    concert_location_service = concert_location_service_test.ConcertLocationServiceTest()
    concert_location_service.test_find_concert_location_by_name_or_create_new()


def concert_time_table_test():
    test = concert_time_table_service_test.ConcertTimeTableServiceTest()
    test.test_creat_concert_time_list()
    # test.test_delete_concert_time_table_by_concert_info_id()


if __name__ == '__main__':
    concert_time_table_test()
