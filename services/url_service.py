from __future__ import annotations

from datetime import timedelta, datetime
from typing import TYPE_CHECKING

from models.short import ShortModel
from services.utils import create_shorten_key

if TYPE_CHECKING:
    from repositories.repository import ShortURLRepository
    from sqlalchemy.orm import Session, Query


class ShortURLService:
    def __init__(self, session_factory, repo: ShortURLRepository):
        self.session_factory = session_factory
        self.repo = repo

    def create_short_model(self, original_url: str, expire_time: int) -> ShortModel:
        with self.session_factory() as session:
            shorten_key = self._get_shorten_key(session, original_url)
            model_obj = ShortModel(
                original_url=original_url,
                expire_at=datetime.now() + timedelta(seconds=expire_time),
                shorten_key=shorten_key
            )
            return self.repo.insert_url(session, model_obj)

    def get_original_url(self, shorten_key: str) -> str:
        with self.session_factory() as session:
            if obj := self._get_shorten_model(session, shorten_key):
                if not obj.is_expired:
                    self.repo.increase_count(session, obj)
                    return obj.original_url
                else:
                    self.repo.soft_delete(session, obj)
            return ""

    def get_shorten_model(self, shorten_key: str) -> ShortModel:
        with self.session_factory() as session:
            obj = self._get_shorten_model(session, shorten_key)
        return obj

    # session 내부 메소드
    def _get_shorten_model(self, session, shorten_key: str) -> ShortModel:
        try:
            result = self._find_by_key(session, shorten_key).one()
        except Exception:
            raise
        return result

    def _get_shorten_key(self, session: Session, original_url: str) -> str:
        shorten_key = create_shorten_key(original_url)
        if not self._exists(session, shorten_key):
            return shorten_key
        return self._get_shorten_key(session, original_url)

    def _exists(self, session: Session, shorten_key: str) -> bool:
        query = self._find_by_key(session, shorten_key)
        return session.query(query.exists()).scalar()

    def _find_by_key(self, session: Session, shorten_key: str) -> Query:
        return session.query(ShortModel).filter(ShortModel.shorten_key == shorten_key,
                                                ShortModel.delete_at == None)
