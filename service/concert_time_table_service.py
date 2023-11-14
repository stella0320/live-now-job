from model.concert_time_table import ConcertTimeTable
from util.db.connect_mysql_db import ConnectDb
from sqlalchemy import delete

from sqlalchemy.ext.declarative import declarative_base


class ConcertTimeTableService():
    
    
    def __init__(self):
        try:
            self.__connect_db__ = ConnectDb()
            self.__engine__ = self.__connect_db__.get_engine()
            self.__session__ = self.__connect_db__.get_session()
        except Exception as e:
            print(f'db error exception {e}')
    def creat_concert_time_list(self, input_list = None):
        if input_list:
            try:
                data_obj = [ConcertTimeTable(**input) for input in input_list]
                self.__session__.add_all(data_obj)
                self.__session__.commit()
                
            except Exception as e:
                self.__session__.rollback()
                print(str(e))

            self.__session__.close()

    # def create_concert_time_list(self, input_list = None):
    #     if input_list:
    #         engine = self.__engine__
    #         with engine.connect() as connection:
    #             with connection.begin():

    #                 stmt = (
    #                         insert(ConcertTimeTable).
    #                         values(input_list)
    #                     )
    #                 connection.execute(stmt)

    def delete_concert_time_table_by_concert_info_id(self, concert_info_id = None):
        if concert_info_id:
            try:
                stmt = delete(ConcertTimeTable).where(ConcertTimeTable.concert_info_id == concert_info_id)
                self.__session__.execute(stmt)
                self.__session__.commit()
            except Exception as e:
                self.__session__.rollback()
                print(str(e))

            # self.__session__.close()

# if __name__ == '__main__':
#     list = [{
#         'concert_info_id': 328,
#         'concert_time_table_type': '演出時間',
#         'concert_time_table_datetime': datetime.date.today()
#     },{
#         'concert_info_id': 328,
#         'concert_time_table_type': '售票時間',
#         'concert_time_table_datetime':datetime.date.today()
#     }]
#     creat_concert_time_list(list)