import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from config import db as db_conf

if os.environ.get('SHOW_SQL_STATEMENTS', '0') != '0':
    import logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class DB:
    def __init__(self):
        self._connection = None
        self._engine = None

    def __del__(self):
        if self._connection:
            self._connection.close()

    @property
    def connetion(self):
        if not self._connection:
            self._connection = sessionmaker(bind=self.engine)()
        return self._connection

    @property
    def engine(self):
        if not self._engine:
            self._engine = create_engine(db_conf.db, poolclass=NullPool)
        return self._engine