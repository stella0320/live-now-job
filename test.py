from serviceTest.concert_info_service_test import ConcertInfoServiceTest


if __name__ == '__main__':
   
    test = ConcertInfoServiceTest()
    # test.test_update_column_values_by_id()
    data = test.test_find_concert_info_by_name()
    print(getattr(data, 'concert_info_id', 'XXX'))

    

    