from datetime import datetime, timedelta

from sqlalchemy import Column, BigInteger, String, Integer, DATETIME, Text

from database import Base


class ShortModel(Base):
    __tablename__ = 'short_model'

    id = Column(Integer, primary_key=True, autoincrement=True)
    shorten_key = Column(String(20), unique=True, nullable=False)
    original_url = Column(Text, nullable=False)
    count = Column(BigInteger, default=0)

    expire_at = Column(DATETIME, default=datetime.now() + timedelta(hours=1))
    delete_at = Column(DATETIME, nullable=True)

    @property
    def is_expired(self) -> bool:
        return True if self.expire_at < datetime.now() else False

    @property
    def is_deleted(self) -> bool:
        return True if self.delete_at is not None else False
