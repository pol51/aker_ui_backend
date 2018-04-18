from sqlalchemy import Column, BigInteger, String

from .base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, nullable=False, primary_key=True)
    
    username = Column(String, unique=True)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<User('{0}')>".format(self.username)
