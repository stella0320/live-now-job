
from ..crawler.tixcraft_crawler import TixcraftCrawler


class TixcraftJob():

    def run(self):
        tixcraftCrawler = TixcraftCrawler()

        # 1. 讀取所有concert soup
        all_concert_element_list = tixcraftCrawler.handle_tixcraft_all_concert()

        # 2. 整理所有concert 基本資訊
        concert_list = tixcraftCrawler.handle_concert_page_to_data(
            all_concert_element_list)

        # 3. 資料和S3不同，再經過chat gpt轉換
        result = []
        if concert_list:
            tixcraftCrawler.save_concert_data(concert_list)

            result = tixcraftCrawler.compare_S3_and_transfer_data_by_chat_gpt()
            print(len(result))

        if len(result) > 0:
            for data in result:
                if data:
                    # 4. 存資料
                    tixcraftCrawler.save_concert_all_data(data)

        # 3.
        # if all_concert_list:
        #     print('-tixCraftCrawler-')
        #     all_concert_json_data = [save_concert_info_data(
        #         concert) for concert in all_concert_list if concert]
        #     print(all_concert_json_data)

        # pass
