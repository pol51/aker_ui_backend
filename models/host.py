from db import db


class Host(db.Model):
    __tablename__ = 'host'

    id = db.Column(db.BigInteger, nullable=False, primary_key=True)
    
    hostname = db.Column(db.String, unique=True)

    def __init__(self, hostname):
        self.hostname = hostname

    def __repr__(self):
        return "<Host('{0}')>".format(self.hostname)
