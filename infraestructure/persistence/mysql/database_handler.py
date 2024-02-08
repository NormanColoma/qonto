from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from infraestructure.config.config import Config


class SqlAlchemyHandler:
    def __init__(self, config: Config):
        self.__config = config

    def get_connection(self):
        try:
            engine = create_engine(
                self.__config.MYSQL_URI,
                isolation_level="READ COMMITTED"
            )
            return Session(engine)
        except Exception as e:
            raise e
