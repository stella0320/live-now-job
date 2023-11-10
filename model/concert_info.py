from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

# 宣告對映
Base = declarative_base()

class ConcertInfo(Base):
    __tablename__ = 'concert_info'
    concert_info_id = Column(Integer, primary_key=True)
    concert_info_status = Column(String(15), nullable=False)
    concert_info_name = Column(String(200), nullable=True)
    concert_info_ticket_system_id = Column(Integer, nullable=True)
    concert_info_location_id = Column(Integer, nullable=False)
    concert_info_singer_id = Column(Integer, nullable=False)
    concert_info_create_time = Column(DateTime, nullable=False)
    concert_info_change_time = Column(DateTime, nullable=False)
    concert_info_page_url = Column(String(300), nullable=False)
    concert_info_image_url = Column(String(300), nullable=False)

    def __repr__(self):
        return f"<concert_info(concert_info_id={self.concert_info_id}, concert_info_name={self.concert_info_name})>"