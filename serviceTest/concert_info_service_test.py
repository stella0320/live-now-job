from service.concert_info_service import ConcertInfoService


class ConcertInfoServiceTest():

    def __init__(self):
        pass

    def test_create_concert_info(self):
        service = ConcertInfoService()

        data_obj = {
            "concert_info_id": 2,
            "concert_info_name": 'MC Hot DogXXX',
            "concert_info_ticket_system_id": 1,
        }
        service.create_concert_info(data_obj)

    def test_update_column_values_by_id(self):
        service2 = ConcertInfoService()
        values =  {
            "concert_info_name": 'MC Hot Dog123',
            "concert_info_ticket_system_id": 2,
        }
        service2.update_column_values_by_id(values, 2)

    def test_query_concert_info_by_id(self):
        
        service3 = ConcertInfoService()
        bean = service3.query_concert_info_by_id(2)
        print(getattr(bean, 'concert_info_name'))

    def test_find_concert_info_by_name(self):
        service4 = ConcertInfoService()
        list = service4.find_concert_info_by_name('MC HotDog熱狗「髒藝術家」2023台北小巨蛋演唱會')
        print(list)
        return list