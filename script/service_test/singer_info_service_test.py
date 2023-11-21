from ..service.singer_info_service import SingerInfoService


class SingerInfoServiceTest():

    def __init__(self):
        pass

    def test_create_singer_info(self):
        service = SingerInfoService()
        singer = {
            "singer_info_name": "MC HOT Dog - TEST"
        }
        service.create_singer_info(singer)

    def test_find_singer_info_by_name(self):
        service = SingerInfoService()
        singer = service.find_singer_info_by_name('MC HOT Dog - TEST')
        print(singer)
        print(type(singer))
        print(getattr(singer, 'singer_info_id'))

    def test_find_singer_info_by_name_or_create_new1(self):
        service = SingerInfoService()
        singer_id = service.find_singer_info_by_name_or_create_new(
            'MC HOT Dog - TEST')
        print(singer_id)

    def test_find_singer_info_by_name_or_create_new2(self):
        service = SingerInfoService()
        singer_id = service.find_singer_info_by_name_or_create_new(
            '徐佳瑩 - TEST')
        print(singer_id)
