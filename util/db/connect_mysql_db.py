from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.orm import sessionmaker
import os


class ConnectDb():

    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.user_name = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        
    # https://docs.sqlalchemy.org/en/20/core/engines.html#mysql
    def get_engine(self):
        try:
            url_object = URL.create(
                    "mysql+pymysql",
                    username=self.user_name,
                    password=self.password,
                    host=self.host,
                    database=os.getenv('DB_DATABASE'),
            )
            engine = create_engine(url_object, pool_size=50)
        except Exception as e:
            print(msg=str(e))
        return engine
    
    def get_session(self):
        engine = self.get_engine()
        Session = sessionmaker(bind=engine)  # 把 DB engine 與 session 綁在一起
        session = Session()
        return session