from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.util.preloaded import orm

Base = declarative_base()


class Database:
    def __init__(self, username, password, address, port, db_name):
        self.engine = create_engine(
            f"mysql+mysqldb://{username}:{password}@{address}:{port}/{db_name}?charset=utf8mb4"
        )
        self.session_factory = orm.scoped_session(orm.sessionmaker(autocommit=False,
                                                                   autoflush=False,
                                                                   bind=self.engine))

    def create_database(self):
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session(self):
        session = self.session_factory()
        try:
            yield session
        except Exception:
            raise
        finally:
            session.close()
