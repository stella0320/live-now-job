from service.concert_location_service import ConcertLocationService

class ConcertLocationServiceTest():

    def test_find_concert_location_by_name_or_create_new(self):
        service = ConcertLocationService()
        location_id = service.find_concert_location_by_name_or_create_new('台北小巨蛋')
        print(location_id)