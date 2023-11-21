from ..crawler.crawler_handle_data import CrawlerHandleData
from .common_crawler import get_page


class TixcraftCrawler():
    crawlerHandleData = None

    def __init__(self):
        pass

    def get_concert_info_html(self, url):
        # 單一場演唱會的頁面
        tixcraft_domain_name = 'https://tixcraft.com'
        concert_page_url = tixcraft_domain_name + url
        concert_text = None
        concert_soup = get_page(concert_page_url)
        if concert_soup:
            activity = concert_soup.select('#intro')
            concert_text = activity[0].get_text()

        return concert_text

    def handle_concert_page_to_data(self, concert_page_list):
        result = []
        for one_concert_page in concert_page_list:
            item = {}
            a = one_concert_page.find('a')

            # 演唱會標題
            titleElement = a.select('.multi_ellipsis')
            if titleElement:
                item['concert_info_name'] = titleElement[0].get_text()

            # 售票連結
            href = a['href']
            item['concert_info_page_url'] = href

            # 演唱會圖片連結
            img_url = a.find('img')['src']
            item['concert_info_image_url'] = img_url
            item['concert_info_ticket_system_id'] = 1
            result.append(item)

        return result

    # 所有演唱會的清單

    def handle_tixcraft_all_concert(self):
        tixcraft_ticket_list_url = 'https://tixcraft.com/activity'
        soup = get_page(tixcraft_ticket_list_url)
        ticket_list = []
        if soup:
            ticket_list = soup.select('.thumbnails')

        return ticket_list

    def save_concert_data(self, concert_list):
        self.crawlerHandleData = CrawlerHandleData(concert_list)
        self.crawlerHandleData.save_concert_info_data()

    def compare_S3_and_transfer_data_by_chat_gpt(self):
        crawlerHandleData = self.crawlerHandleData
        result = []
        if crawlerHandleData:
            result = self.crawlerHandleData.compare_S3_and_transfer_data_by_chat_gpt(
                self.get_concert_info_html)
        return result

    def save_concert_all_data(self, concert_data):
        self.crawlerHandleData.save_concert_all_data(concert_data)
