from ..model.singer_info import SingerInfo
from ..util.db.connect_mysql_db import ConnectDb
from sqlalchemy import MetaData, Table, update, select
from ..api.kkbox_api import KkboxApi
from script.api import kkbox_api


class SingerInfoService():

    def __init__(self):
        try:
            self.__connect_db__ = ConnectDb()
            self.__engine__ = self.__connect_db__.get_engine()
            self.__session__ = self.__connect_db__.get_session()
        except Exception as e:
            print(f'exception {e}')

    def create_singer_info(self, data_obj=None):
        if data_obj:
            try:
                self.__session__.add(SingerInfo(**data_obj))
                self.__session__.commit()
            except Exception as e:
                self.__session__.rollback()
                print(str(e))

            self.__session__.close()

    def update_all_singer_image(self):
        all_singer_info = self.__session__.query(SingerInfo).all()
        kkbox_api = KkboxApi()
        update_data_list = []
        for singer_info in all_singer_info:
            singer_info_name = getattr(singer_info, 'singer_info_name')
            print(singer_info_name)
            singer_image_url = kkbox_api.search_image_url_by_singer_name_retry(
                singer_info_name)
            if singer_image_url:
                singer_info_id = getattr(singer_info, 'singer_info_id')
                obj = {
                    'singer_info_id': singer_info_id,
                    'singer_info_image_url': singer_image_url
                }
                update_data_list.append(obj)

        if update_data_list:
            self.__session__.execute(
                update(SingerInfo), update_data_list, )
            self.__session__.commit()
        self.__session__.close()

    def find_singer_info_by_name(self, name):
        singer = None
        if name:
            try:
                singer = self.__session__.query(SingerInfo).filter_by(
                    singer_info_name=name).first()
            except Exception as e:
                print(str(e))
            self.__session__.close()

        return singer

    def find_singer_info_by_name_or_create_new(self, name):
        singer = None
        if name:
            try:
                singer = self.__session__.query(SingerInfo).filter_by(
                    singer_info_name=name).first()
            except Exception as e:
                print(str(e))

        if not singer and name:
            try:
                kkbox_api = KkboxApi()
                singer_image_url = kkbox_api.search_image_url_by_singer_name_retry(
                    name)
                data_obj = {
                    'singer_info_name': name,
                    'singer_info_image_url': singer_image_url
                }
                self.__session__.add(SingerInfo(**data_obj))
                self.__session__.commit()
                singer = self.__session__.query(SingerInfo).filter_by(
                    singer_info_name=name).first()

            except Exception as e:
                self.__session__.rollback()
                print(str(e))
            finally:
                self.__session__.close()
        if singer:
            return getattr(singer, 'singer_info_id', None)

        return None
