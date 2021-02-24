import logging.config
import re
from functools import wraps
from typing import List, NoReturn, Optional

from sqlalchemy import create_engine, func
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from redshift import cfg
from redshift.log_maker import LogMaker
from redshift.models.base import Base
from redshift.models.tables import Users, Venue, Category, Date, Event, \
    Listing, Sales
from redshift.singleton_meta import SingletonMeta

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

    def __init__(self, echo=False):
        self._engine: Engine = create_engine(
            f'redshift+psycopg2://{cfg.RS_USR}:{cfg.RS_PWD}'
            f'@{cfg.RS_HOST}:{cfg.RS_PORT}/{cfg.RS_DB}',
            echo=echo,
            echo_pool=echo,
            pool_size=20,
            max_overflow=5,
            pool_recycle=3600,
            pool_timeout=30)

    def _get_session(self) -> Session:
        _Session = sessionmaker(bind=self._engine)
        return _Session()

    @log_maker
    def reset_engine(self) -> NoReturn:
        """Dispose of the connection pool

        """
        self._engine.dispose()

    @log_maker
    def create_all(self) -> NoReturn:
        Base.metadata.create_all(self._engine)

    @log_maker
    def drop_all(self) -> NoReturn:
        """drop all tables defined in `redshift.tables`

        there's no native `DROP TABLE ... CASCADE ...` method and tables should
        be dropped from the leaves of the dependency tree back to the root
        """
        tables = (Sales, Listing, Event, Users, Venue, Category, Date)
        list(
            map(
                lambda tb: tb.__table__.drop(bind=self._engine,
                                             checkfirst=True), tables))

    @log_maker
    def all_tables(self) -> List[str]:
        return self._engine.table_names()

    @log_maker
    def load_sample(self) -> NoReturn:
        def statement(table: str, filename: str, delimiter: str,
                      timeformat: str) -> str:
            return f'''copy {table} from
                's3://{cfg.S3_BUCKET}/tickit/{filename}'
                credentials 'aws_iam_role={cfg.RS_IAM_ROLE}'
                delimiter '{delimiter}' {timeformat}
                region '{cfg.S3_REGION}';
                '''

        dlm_map = {'pipe': '|', 'tab': '\\t'}
        tables = [
            'users', 'venue', 'category', 'date', 'event', 'listing', 'sales'
        ]
        files = [
            'allusers_pipe.txt',
            'venue_pipe.txt',
            'category_pipe.txt',
            'date2008_pipe.txt',
            'allevents_pipe.txt',
            'listings_pipe.txt',
            'sales_tab.txt',
        ]
        delimiters = [
            dlm_map[next(
                filter(lambda i: i in ['pipe', 'tab'], re.split(r'[_.]', s)))]
            for s in files
        ]
        formats = [
            '', '', '', '', "timeformat 'YYYY-MM-DD HH:MI:SS'", '',
            "timeformat 'MM/DD/YYYY HH:MI:SS'"
        ]
        with self._engine.begin() as conn:
            for tb, file, dlm, fmt in zip(tables, files, delimiters, formats):
                conn.execute(statement(tb, file, dlm, fmt))

    @log_maker
    def all_users(self) -> List[Users]:
        @_commit
        def _all_users(session: Session):
            return session.query(Users).all()

        return _all_users(self._get_session())

    @log_maker
    def count_users(self) -> Optional[int]:
        @_commit
        def helper(session: Session):
            return session.query(func.count(Users.userid)).scalar()

        return helper(self._get_session())

    @log_maker
    def count_venue(self) -> Optional[int]:
        @_commit
        def helper(session: Session):
            return session.query(func.count(Venue.venueid)).scalar()

        return helper(self._get_session())

    @log_maker
    def count_category(self) -> Optional[int]:
        @_commit
        def helper(session: Session):
            return session.query(func.count(Category.catid)).scalar()

        return helper(self._get_session())

    @log_maker
    def count_date(self) -> Optional[int]:
        @_commit
        def helper(session: Session):
            return session.query(func.count(Date.dateid)).scalar()

        return helper(self._get_session())

    @log_maker
    def count_event(self) -> Optional[int]:
        @_commit
        def helper(session: Session):
            return session.query(func.count(Event.eventid)).scalar()

        return helper(self._get_session())

    @log_maker
    def count_listing(self) -> Optional[int]:
        @_commit
        def helper(session: Session):
            return session.query(func.count(Listing.listid)).scalar()

        return helper(self._get_session())

    @log_maker
    def count_sales(self) -> Optional[int]:
        @_commit
        def helper(session: Session):
            return session.query(func.count(Sales.salesid)).scalar()

        return helper(self._get_session())

    @log_maker
    def total_sales(self, dt: str) -> Optional[int]:
        """total sales on a given calendar date.

        :param dt: date string formatted as 'yyyy-mm-dd'
        :return: total sales on that day
        """
        @_commit
        def helper(session: Session):
            return session.query(func.sum(
                Sales.qtysold).label('total_sold')).join(
                    Date, Sales.dateid == Date.dateid).filter(
                        Date.caldate == dt).scalar()

        return helper(self._get_session())
