from sqlalchemy.orm import relationship
from sqlalchemy import Column, BigInteger, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID

from .base import Base
from .user import User
from .host import Host


class Session(Base):
    __tablename__ = 'session'

    uuid = Column(UUID, nullable=False, primary_key=True)
    
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    user = relationship(User, foreign_keys=[user_id])

    host_id = Column(BigInteger, ForeignKey('host.id'), nullable=False)
    host = relationship(Host, foreign_keys=[user_id])

    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    
    @property
    def duration(self):
      return self.end - self.start
    
    def __repr__(self):
        return "<Session(uuid='{0}', user='{1}', host='{2}', start='{3}', duration='{4}')>".format(self.uuid, self.user.username, self.host, self.start, self.duration)
