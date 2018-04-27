from sqlalchemy.orm import backref
from sqlalchemy.dialects.postgresql import UUID

from db import db
from .session import Session


class Command(db.Model):
    __tablename__ = 'command'

    id = db.Column(db.BigInteger, nullable=False, primary_key=True)

    timing = db.Column(db.DateTime, nullable=False)
    cmd = db.Column(db.String, nullable=False)

    session_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('session.uuid'), nullable=False)
    session = db.relationship(Session, foreign_keys=[session_uuid], backref=backref('commands', lazy='dynamic'))

    def __init__(self, session, cmd, timing):
        self.session = session
        self.cmd = cmd
        self.timing = timing

    def __repr__(self):
        return "<Command(cmd='{0}', session='{1}')>".format(self.cmd, self.session)
