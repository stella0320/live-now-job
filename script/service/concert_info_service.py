from ..model.concert_info import ConcertInfo
from ..util.db.connect_mysql_db import ConnectDb
from sqlalchemy import MetaData, Table, update, select


class ConcertInfoService():

    def __init__(self):
        try:
            self.__connect_db__ = ConnectDb()
            self.__engine__ = self.__connect_db__.get_engine()
            self.__session__ = self.__connect_db__.get_session()
        except Exception as e:
            print(f'exception {e}')

    def get_column_name(self):
        metadata = MetaData()
        engine = self.__engine__
        table = Table('concert_info', metadata,
                      autoload=True, autoload_with=engine)

        # Access the column names
        column_names = table.columns.keys()
        return column_names

    def create_concert_info(self, data_obj=None):
        if data_obj:
            try:
                self.__session__.add(ConcertInfo(**data_obj))
                self.__session__.commit()
            except Exception as e:
                self.__session__.rollback()
                print(f'exception {e}')
            finally:
                self.__session__.close()

    def update_column_values_by_id(self, update_values, primary_key_value):
        if primary_key_value and update_values:
            try:
                stmt = update(ConcertInfo).where(
                    ConcertInfo.concert_info_id == primary_key_value).values(update_values)
                self.__session__.execute(stmt)
                self.__session__.commit()
            except Exception as e:
                self.__session__.rollback()
                print(f'exception {e}')
            finally:
                self.__session__.close()

    def query_concert_info_by_id(self, concert_info_id):

        concert_info = None
        if concert_info_id:
            try:
                concert_info = self.__session__.query(
                    ConcertInfo).get(concert_info_id)
            except Exception as e:
                print(f'exception {e}')
            finally:
                self.__session__.close()

        return concert_info

    def find_concert_info_by_name(self, name):
        list = None
        if name:
            try:
                list = self.__session__.query(ConcertInfo).filter_by(
                    concert_info_name=name).all()
            except Exception as e:
                print(f'exception {e}')
            finally:
                self.__session__.close()

        return list
