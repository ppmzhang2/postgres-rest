from datetime import datetime

from sqlalchemy import (CHAR, DECIMAL, TIMESTAMP, VARCHAR, Boolean, Column,
                        Date, ForeignKey, Integer, MetaData, Sequence,
                        SmallInteger, Table)

metadata = MetaData()

dateid_seq = Sequence('dateid_seq', start=1827, increment=1)

users = Table(
    'd_user',
    metadata,
    Column('userid', Integer, primary_key=True),
    Column('username', CHAR(length=8)),
    Column('firstname', VARCHAR(length=30)),
    Column('lastname', VARCHAR(length=30)),
    Column('city', VARCHAR(length=30)),
    Column('state', CHAR(length=2)),
    Column('email', VARCHAR(length=100)),
    Column('phone', CHAR(length=14)),
    Column('likesports', Boolean),
    Column('liketheatre', Boolean),
    Column('likeconcerts', Boolean),
    Column('likejazz', Boolean),
    Column('likeclassical', Boolean),
    Column('likeopera', Boolean),
    Column('likerock', Boolean),
    Column('likevegas', Boolean),
    Column('likebroadway', Boolean),
    Column('likemusicals', Boolean),
)

venues = Table(
    'd_venue',
    metadata,
    Column('venueid', Integer, primary_key=True),
    Column('venuename', VARCHAR(100)),
    Column('venuecity', VARCHAR(30)),
    Column('venuestate', CHAR(2)),
    Column('venueseats', Integer),
)

categories = Table(
    'd_category',
    metadata,
    Column('catid', Integer, primary_key=True),
    Column('catgroup', VARCHAR(10)),
    Column('catname', VARCHAR(10)),
    Column('catdesc', VARCHAR(50)),
)

dates = Table(
    'd_date',
    metadata,
    Column('dateid',
           Integer,
           dateid_seq,
           server_default=dateid_seq.next_value(),
           primary_key=True),
    Column('caldate', Date, nullable=False),
    Column('day', CHAR(3), nullable=False),
    Column('week', SmallInteger, nullable=False),
    Column('month', CHAR(5), nullable=False),
    Column('qtr', CHAR(5), nullable=False),
    Column('year', SmallInteger, nullable=False),
    Column('holiday', Boolean, default=False),
)

events = Table(
    'f_event',
    metadata,
    Column('eventid', Integer, primary_key=True),
    Column(
        'venueid',
        Integer,
        ForeignKey('d_venue.venueid', onupdate='CASCADE', ondelete='CASCADE'),
    ),
    Column(
        'catid',
        Integer,
        ForeignKey('d_category.catid', onupdate='CASCADE', ondelete='CASCADE'),
    ),
    Column(
        'dateid',
        Integer,
        ForeignKey('d_date.dateid', onupdate='CASCADE', ondelete='CASCADE'),
    ),
    Column('eventname', VARCHAR(200)),
    Column('starttime', TIMESTAMP, default=datetime.now),
)

listings = Table(
    'f_listing',
    metadata,
    Column('listid', Integer, primary_key=True),
    Column('sellerid', Integer, nullable=False),
    Column(
        'eventid',
        Integer,
        ForeignKey('f_event.eventid', onupdate='CASCADE', ondelete='CASCADE'),
    ),
    Column(
        'dateid',
        Integer,
        ForeignKey('d_date.dateid', onupdate='CASCADE', ondelete='CASCADE'),
    ),
    Column('numtickets', SmallInteger, nullable=False),
    Column('priceperticket', DECIMAL(8, 2)),
    Column('totalprice', DECIMAL(8, 2)),
    Column('listtime', TIMESTAMP),
)

sales = Table(
    'f_sale',
    metadata,
    Column('salesid', Integer, primary_key=True),
    Column(
        'listid',
        Integer,
        ForeignKey('f_listing.listid', onupdate='CASCADE', ondelete='CASCADE'),
    ),
    Column('sellerid', Integer, nullable=False),
    Column('buyerid', Integer, nullable=False),
    Column(
        'eventid',
        Integer,
        ForeignKey('f_event.eventid', onupdate='CASCADE', ondelete='CASCADE'),
    ),
    Column(
        'dateid',
        Integer,
        ForeignKey('d_date.dateid', onupdate='CASCADE', ondelete='CASCADE'),
    ),
    Column('qtysold', SmallInteger, nullable=False),
    Column('pricepaid', DECIMAL(8, 2)),
    Column('commission', DECIMAL(8, 2)),
    Column('saletime', TIMESTAMP),
)
