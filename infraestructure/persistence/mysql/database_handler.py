from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from infraestructure.config.config import Config


class SqlAlchemyHandler:
    def __init__(self, config: Config):
        self.__config = config

    @contextmanager
    def get_connection(self):
        try:
            engine = create_engine(
                self.__config.MYSQL_URI,
                isolation_level="READ COMMITTED"
            )
            session = Session(engine)
            yield session
        except Exception as e:
            session.rollback()
            raise e
        else:
            session.commit()
