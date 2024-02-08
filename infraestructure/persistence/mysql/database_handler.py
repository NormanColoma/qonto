from contextlib import contextmanager

import sqlalchemy

from infraestructure.config.config import Config


class SqlAlchemyHandler:
    def __init__(self, config: Config, sql_client: sqlalchemy):
        self.__config = config
        self.__client = sql_client

    @contextmanager
    def get_connection(self):
        try:
            engine = self.__client.create_engine(
                self.__config.MYSQL_URI,
                isolation_level="READ COMMITTED"
            )
            session = self.__client.orm.Session(engine)
            yield session
        except Exception as e:
            session.rollback()
            raise e
        else:
            session.commit()
