from script.service.singer_info_service import SingerInfoService

if __name__ == "__main__":
    service = SingerInfoService()
    service.update_all_singer_image()