from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from models.short import ShortModel

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class ShortURLRepository:
    def insert_url(self, session: Session, obj: ShortModel) -> ShortModel:
        try:
            session.add(obj)
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        session.refresh(obj)
        return obj

    def increase_count(self, session: Session, obj: ShortModel) -> None:
        update_model = session.query(ShortModel).filter(ShortModel.id == obj.id).with_for_update().one()
        update_model.count += 1
        session.commit()

    def soft_delete(self, session: Session, obj: ShortModel) -> None:
        obj.delete_at = datetime.now()
        session.commit()

    def hard_delete(self, session: Session, obj: ShortModel) -> None:
        session.delete(obj)
        session.commit()
