import os

from dependency_injector import containers, providers

from database import Database
from repositories.repository import ShortURLRepository
from services.url_service import ShortURLService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["api"])
    config = providers.Configuration(yaml_files=["config.yml"])
    db = providers.Singleton(
        Database,
        username=os.environ.get("DB_USERNAME", config.db.username),
        password=os.environ.get("DB_PASSWORD", config.db.password),
        address=os.environ.get("DB_HOST", config.db.address),
        port=os.environ.get("DB_PORT", config.db.port),
        db_name=os.environ.get("DB_NAME", config.db.db_name),
    )
    short_repository = providers.Factory(ShortURLRepository)
    short_service = providers.Factory(ShortURLService,
                                      repo=short_repository,
                                      session_factory=db.provided.session)
