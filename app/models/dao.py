import logging
import re
from typing import Any, List, NoReturn, Optional, Sequence

from sqlalchemy import Column, Table, func
from sqlalchemy.engine.result import RowProxy
from sqlalchemy.sql import select

from app import cfg
from app.log_maker import LogMaker
from app.models.session import safe_session
from app.models.tables import (categories, dates, events, listings, sales,
                               users, venues)
from app.schema.api_exception import ApiException, ErrorCategory

__all__ = ['Dao']

logging.config.dictConfig(cfg.LOGGING)
logger = logging.getLogger('info_logger')
log_maker = LogMaker(logger)


class Dao:
    @staticmethod
    def _exec(stmt: str, *args, **kwargs):
        try:
            with safe_session() as sess:
                res = sess.execute(stmt, *args, **kwargs)
            return res
        except Exception as exc:
            raise ApiException(500, ErrorCategory.DB_OTHER, repr(exc)) from exc

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
            self._exec(statement(tb, col, f, dlm))

    def _all(self, table: Table, limit: int, offset: int) -> List[RowProxy]:
        res = self._exec(select([table]).limit(limit).offset(offset))
        return res.fetchall()

    @log_maker
    def all_user(self, limit: int, offset: int) -> List[RowProxy]:
        return self._all(users, limit, offset)

    @log_maker
    def all_category(self, limit: int, offset: int) -> List[RowProxy]:
        return self._all(categories, limit, offset)

    def _count(self, column: Column) -> int:
        stmt = select([func.count(column)])
        res = self._exec(stmt)
        return res.first()[0]

    def _lookup(
        self,
        table: Table,
        column: Column,
        key: Any,
    ) -> Optional[RowProxy]:
        stmt = select([table]).where(column == key)
        res = self._exec(stmt).first()
        if not res:
            raise ApiException(
                404,
                ErrorCategory.NOT_FOUND,
                (f'no record with filter "{column.name} = {key}" in '
                 f'"{table.name}"'),
            )
        return res

    def _insert_one(self, table: Table, pkid: str, **kwargs) -> int:
        """insert one record into table and return its primary key

        :param table: table object to be inserted
        :param kwargs: column-value pairs, each key must match its
            corresponding column name
        :return:
        """
        stmt = table.insert().values(**kwargs).returning(table.columns[pkid])
        res = self._exec(stmt)
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

    def total_sales_amount(self, dt: str) -> int:
        """total sales on a given calendar date.

        :param dt: date string formatted as 'yyyy-mm-dd'
        :return: total sales on that day
        """
        stmt = select([func.sum(sales.c.qtysold).label('total_sold')
                       ]).where(dates.c.caldate == dt).select_from(
                           sales.join(dates, sales.c.dateid == dates.c.dateid))
        res = self._exec(stmt)
        return res.first()[0] or 0
