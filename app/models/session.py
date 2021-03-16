from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import cfg

# for postgres, connection timeout on 2 min
engine = create_engine(
    f'postgresql+psycopg2://{cfg.SA_USR}:{cfg.SA_PWD}'
    f'@{cfg.SA_HOST}:{cfg.SA_PORT}/{cfg.SA_DB}',
    echo=False,
    echo_pool=False,
    pool_size=20,
    max_overflow=5,
    pool_recycle=3600,
    pool_timeout=30,
    connect_args={"options": "-c statement_timeout=120000"},
)

Session = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


# TODO: to invalidate when connection timeout instead of just closing
# i.e. give back to the connection pool the unusable connection
@contextmanager
def safe_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as exc:
        session.roll_back()
        raise exc
    finally:
        session.close()
