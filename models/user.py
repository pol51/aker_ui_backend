from db import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.BigInteger, nullable=False, primary_key=True)
    
    username = db.Column(db.String, unique=True)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<User('{0}')>".format(self.username)
