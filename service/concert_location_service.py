from model.concert_location import ConcertLocation
from util.db.connect_mysql_db import ConnectDb
from sqlalchemy import MetaData, Table, update, select

class ConcertLocationService():
    
    def __init__(self):
        try:
            self.__connect_db__ = ConnectDb()
            self.__engine__ = self.__connect_db__.get_engine()
            self.__session__ = self.__connect_db__.get_session()
        except Exception as e:
            print(f'db error exception {e}')

    def find_concert_location_by_name_or_create_new(self, name):
        concert_location = None
        if name:
            try:
                concert_location = self.__session__.query(ConcertLocation).filter_by(concert_location_name=name).first()
            except Exception as e:
                print(str(e))
        
                

        if not concert_location and name:
            try:
                self.__session__.add(ConcertLocation(name))
                self.__session__.commit()
                concert_location = self.__session__.query(ConcertLocation).filter_by(concert_location_name=name).first()
                
            except Exception as e:
                self.__session__.rollback()
                print(str(e))
        
        self.__session__.close()

        if concert_location:
            return getattr(concert_location, 'concert_location_id')
        
        return None