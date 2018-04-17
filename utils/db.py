from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from config import db as db_conf


class DB:
    def __init__(self):
        self._connection = None

    def __del__(self):
        if self._connection:
            self._connection.close()

    @property
    def connetion(self):
        if not self._connection:
            engine = create_engine(db_conf.db, poolclass=NullPool)
            self._connection = sessionmaker(bind=engine)()
        return self._connection