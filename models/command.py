from sqlalchemy.orm import relationship
from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID

from .base import Base
from .session import Session


class Command(Base):
    __tablename__ = 'command'

    id = Column(BigInteger, nullable=False, primary_key=True)

    timing = Column(DateTime, nullable=False)
    cmd = Column(String, nullable=False)

    session_uuid = Column(UUID, ForeignKey('session.uuid'), nullable=False)
    session = relationship(Session, foreign_keys=[session_uuid])

    def __init__(self, session, cmd, timing):
        self.session = session
        self.cmd = cmd
        self.timing = timing

    def __repr__(self):
        return "<Command(cmd='{0}', session='{1}')>".format(self.cmd, self.session)
