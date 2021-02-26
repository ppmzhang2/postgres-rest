import logging.config
import re
from functools import wraps
from typing import Any, List, NoReturn, Optional, Sequence

from sqlalchemy import Column, Table, create_engine, func
from sqlalchemy.engine import Engine
from sqlalchemy.engine.result import RowProxy
from sqlalchemy.sql import select

from postgres import cfg
from postgres.log_maker import LogMaker
from postgres.models.tables import (categories, dates, events, listings, sales,
                                    users, venues)
from postgres.singleton_meta import SingletonMeta

__all__ = ['Dao']

logging.config.dictConfig(cfg.LOGGING)
logger = logging.getLogger('info_logger')
log_maker = LogMaker(logger)


def _commit(fn):
    @wraps(fn)
    def helper(*args, **kwargs):
        res = fn(*args, **kwargs)
        args[0].commit()
        return res

    return helper


class Dao(metaclass=SingletonMeta):
    __slots__ = ['_engine']

    _TABLES = (sales, listings, events, users, venues, categories, dates)

    def __init__(self, echo=False):
        self._engine: Engine = create_engine(
            f'postgresql+psycopg2://{cfg.SA_USR}:{cfg.SA_PWD}'
            f'@{cfg.SA_HOST}:{cfg.SA_PORT}/{cfg.SA_DB}',
            echo=echo,
            echo_pool=echo,
            pool_size=20,
            max_overflow=5,
            pool_recycle=3600,
            pool_timeout=30)

    def _exec_stmt(self, stmt: str, *args, **kwargs):
        with self._engine.begin() as conn:
            res = conn.execute(stmt, *args, **kwargs)
        return res

    @log_maker
    def reset_engine(self) -> NoReturn:
        """Dispose of the connection pool

        """
        self._engine.dispose()

    @log_maker
    def create_all(self) -> NoReturn:
        for table in reversed(self._TABLES):
            table.create(bind=self._engine, checkfirst=True)

    @log_maker
    def drop_all(self) -> NoReturn:
        """drop all tables defined in `redshift.tables`

        there's no native `DROP TABLE ... CASCADE ...` method and tables should
        be dropped from the leaves of the dependency tree back to the root
        """
        for table in self._TABLES:
            table.drop(bind=self._engine, checkfirst=True)

    @log_maker
    def all_tables(self) -> List[str]:
        return self._engine.table_names()

    @log_maker
    def load_sample(self) -> NoReturn:
        def not_primaries(table: Table):
            return list(
                col.key
                for col in filter(lambda x: not x.primary_key, table.c))

        def statement(table: str, columns: Sequence[str], filename: str,
                      delimiter: str) -> str:
            return f'''copy {table}({','.join(columns)}) from
                '/etc/data/{filename}'
                delimiter {delimiter} CSV;
                '''

        dlm_map = {'pipe': "'|'", 'tab': "E'\\t'"}
        tables = {
            'd_user': users,
            'd_venue': venues,
            'd_category': categories,
            'd_date': dates,
            'f_event': events,
            'f_listing': listings,
            'f_sale': sales,
        }
        files = [
            'allusers_pipe.txt',
            'venue_pipe.txt',
            'category_pipe.txt',
            'date2008_pipe.txt',
            'allevents_pipe.txt',
            'listings_pipe.txt',
            'sales_tab.txt',
        ]
        columns = [not_primaries(t) for t in tables.values()]
        delimiters = [
            dlm_map[next(
                filter(lambda i: i in ['pipe', 'tab'], re.split(r'[_.]', s)))]
            for s in files
        ]
        for tb, col, f, dlm in zip(tables.keys(), columns, files, delimiters):
            self._exec_stmt(statement(tb, col, f, dlm))

    @log_maker
    def all_users(self) -> List[RowProxy]:
        res = self._exec_stmt(select([users]))
        return res.fetchall()

    def _count(self, column: Column) -> int:
        stmt = select([func.count(column)])
        res = self._exec_stmt(stmt)
        return res.first()[0]

    def _lookup(
        self,
        table: Table,
        column: Column,
        key: Any,
    ) -> Optional[RowProxy]:
        stmt = select([table]).where(column == key)
        res = self._exec_stmt(stmt).first()
        if not res:
            return None
        return res

    def _insert_one(self, table: Table, pkid: str, **kwargs) -> int:
        """insert one record into table and return its primary key

        :param table: table object to be inserted
        :param kwargs: column-value pairs, each key must match its
            corresponding column name
        :return:
        """
        stmt = table.insert().values(**kwargs).returning(table.columns[pkid])
        res = self._exec_stmt(stmt)
        return res.first()[0]

    @log_maker
    def add_category(self, group: str, name: str, desc: str) -> int:
        return self._insert_one(categories,
                                'catid',
                                catgroup=group,
                                catname=name,
                                catdesc=desc)

    @log_maker
    def lookup_category_id(self, cat_id: int) -> Optional[RowProxy]:
        return self._lookup(categories, categories.c.catid, cat_id)

    @log_maker
    def lookup_category_name(self, cat_name: str) -> Optional[RowProxy]:
        return self._lookup(categories, categories.c.catname, cat_name)

    @log_maker
    def count_users(self) -> int:
        return self._count(users.c.userid)

    @log_maker
    def count_venues(self) -> int:
        return self._count(venues.c.venueid)

    @log_maker
    def count_categories(self) -> int:
        return self._count(categories.c.catid)

    @log_maker
    def count_dates(self) -> int:
        return self._count(dates.c.dateid)

    @log_maker
    def count_events(self) -> int:
        return self._count(events.c.eventid)

    @log_maker
    def count_listings(self) -> int:
        return self._count(listings.c.listid)

    @log_maker
    def count_sales(self) -> int:
        return self._count(sales.c.salesid)

    @log_maker
    def total_sales_amount(self, dt: str) -> Optional[int]:
        """total sales on a given calendar date.

        :param dt: date string formatted as 'yyyy-mm-dd'
        :return: total sales on that day
        """
        stmt = select([func.sum(sales.c.qtysold).label('total_sold')
                       ]).where(dates.c.caldate == dt).select_from(
                           sales.join(dates, sales.c.dateid == dates.c.dateid))
        return self._exec_stmt(stmt).first()[0]
