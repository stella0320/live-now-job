from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime


Base = declarative_base()

class ConcertTimeTable(Base):
    __tablename__ = 'concert_time_table'
    concert_time_table_id = Column(Integer, primary_key=True)
    concert_info_id = Column(Integer, nullable=False)
    concert_time_table_type = Column(String(10), nullable=False)
    concert_time_table_description = Column(String(30), nullable=False)
    concert_time_table_datetime = Column(DateTime, nullable=False)

