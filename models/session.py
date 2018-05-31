from sqlalchemy.orm import backref
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property

from db import db
from .user import User
from .host import Host


class Session(db.Model):
    __tablename__ = 'session'

    uuid = db.Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, foreign_keys=[user_id], backref=backref('sessions', lazy='dynamic'))

    host_id = db.Column(db.BigInteger, db.ForeignKey('host.id'), nullable=False)
    host = db.relationship(Host, foreign_keys=[host_id], backref=backref('sessions', lazy='dynamic'))

    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)

    def __init__(self, uuid, user, host, start, end):
        self.uuid = uuid
        self.user = user
        self.host = host
        self.start = start
        self.end = end
    
    @hybrid_property
    def duration(self):
        return self.end - self.start

    def __repr__(self):
        return "<Session(uuid='{0}', user='{1}', host='{2}', start='{3}', duration='{4}')>".format(self.uuid, self.user.username, self.host.hostname, self.start, self.duration)
