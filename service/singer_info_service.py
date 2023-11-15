from model.singer_info import SingerInfo
from util.db.connect_mysql_db import ConnectDb
from sqlalchemy import MetaData, Table, update, select


class SingerInfoService():

    def __init__(self):
        try:
            self.__connect_db__ = ConnectDb()
            self.__engine__ = self.__connect_db__.get_engine()
            self.__session__ = self.__connect_db__.get_session()
        except Exception as e:
            print(f'exception {e}')


    def create_singer_info(self, data_obj = None):
        if data_obj:
            try:
                self.__session__.add(SingerInfo(**data_obj))
                self.__session__.commit()
            except Exception as e:
                self.__session__.rollback()
                print(str(e))

            self.__session__.close()


    def find_singer_info_by_name(self, name):
        singer = None
        if name:
            try:
                singer = self.__session__.query(SingerInfo).filter_by(singer_info_name=name).first()
            except Exception as e:
                print(str(e))
            self.__session__.close()
        
        return singer
    

    def find_singer_info_by_name_or_create_new(self, name):
        singer = None
        if name:
            try:
                singer = self.__session__.query(SingerInfo).filter_by(singer_info_name=name).first()
            except Exception as e:
                print(str(e))
        
        if not singer and name:
            try:
                self.__session__.add(SingerInfo(name))
                self.__session__.commit()
                singer = self.__session__.query(SingerInfo).filter_by(singer_info_name=name).first()

            except Exception as e:
                self.__session__.rollback()
                print(str(e))
            finally:
                self.__session__.close()
        if singer:
            return getattr(singer, 'singer_info_id', None)
        
        return None