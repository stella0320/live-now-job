from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class SingerInfo(Base):
    __tablename__ = 'singer_info'
    singer_info_id = Column(Integer, primary_key=True)
    singer_info_name = Column(String(300), nullable=False)
    singer_info_image_url = Column(String(1000), nullable=True)

    def __repr__(self):
        return f"<singer_info(singer_info_id={self.singer_info_id}, singer_info_name={self.singer_info_name})>"
    