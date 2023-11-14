from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class ConcertLocation(Base):
    __tablename__ = 'concert_location'
    concert_location_id = Column(Integer, primary_key=True)
    concert_location_name = Column(String(30), nullable=False)
    
    def __init__(self, name):
        self.concert_location_name = name

    def __repr__(self):
        return f"<concert_location(concert_location_id={self.concert_location_id}, concert_location_name={self.concert_location_name})>"