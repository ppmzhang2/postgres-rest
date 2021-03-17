import logging.config
from typing import List, NoReturn

from app import cfg
from app.models.session import engine
from app.models.tables import (categories, dates, events, listings, sales,
                               users, venues)

__all__ = ['DB']

logging.config.dictConfig(cfg.LOGGING)
logger = logging.getLogger('info_logger')


class DB:
    _TABLES = (sales, listings, events, users, venues, categories, dates)

    @staticmethod
    def all_tables() -> List[str]:
        return engine.table_names()

    @classmethod
    def create_all(cls) -> NoReturn:
        for table in reversed(cls._TABLES):
            table.create(bind=engine, checkfirst=True)

    @classmethod
    def drop_all(cls) -> NoReturn:
        """drop all tables defined in `redshift.tables`

        there's no native `DROP TABLE ... CASCADE ...` method and tables should
        be dropped from the leaves of the dependency tree back to the root
        """
        for table in cls._TABLES:
            table.drop(bind=engine, checkfirst=True)
