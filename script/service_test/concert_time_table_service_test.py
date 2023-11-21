from ..service.concert_time_table_service import ConcertTimeTableService
import datetime


class ConcertTimeTableServiceTest():

    def test_creat_concert_time_list(self):
        list = [{
            'concert_info_id': 328,
            'concert_time_table_type': '演出時間',
            'concert_time_table_datetime': datetime.date.today()
        }, {
            'concert_info_id': 328,
            'concert_time_table_type': '售票時間',
            'concert_time_table_datetime': datetime.date.today()
        }]

        service = ConcertTimeTableService()
        service.creat_concert_time_list(list)

    def test_delete_concert_time_table_by_concert_info_id(self):
        service = ConcertTimeTableService()
        service.delete_concert_time_table_by_concert_info_id(328)
