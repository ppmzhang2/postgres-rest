import datetime

import sqlalchemy as sa
from sqlalchemy import ForeignKey

from redshift.models.base import Base


class Users(Base):
    __tablename__ = 'users'

    userid = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.CHAR(length=8))
    firstname = sa.Column(sa.VARCHAR(length=30))
    lastname = sa.Column(sa.VARCHAR(length=30))
    city = sa.Column(sa.VARCHAR(length=30))
    state = sa.Column(sa.CHAR(length=2))
    email = sa.Column(sa.VARCHAR(length=100))
    phone = sa.Column(sa.CHAR(length=14))
    likesports = sa.Column(sa.Boolean)
    liketheatre = sa.Column(sa.Boolean)
    likeconcerts = sa.Column(sa.Boolean)
    likejazz = sa.Column(sa.Boolean)
    likeclassical = sa.Column(sa.Boolean)
    likeopera = sa.Column(sa.Boolean)
    likerock = sa.Column(sa.Boolean)
    likevegas = sa.Column(sa.Boolean)
    likebroadway = sa.Column(sa.Boolean)
    likemusicals = sa.Column(sa.Boolean)

    __table_args__ = {
        'redshift_sortkey': 'userid',
        'redshift_distkey': 'userid',
    }

    def __init__(
        self,
        userid: int,
        username: str,
        firstname: str,
        lastname: str,
        city: str,
        state: str,
        email: str,
        phone: str,
        likesports: bool,
        liketheatre: bool,
        likeconcerts: bool,
        likejazz: bool,
        likeclassical: bool,
        likeopera: bool,
        likerock: bool,
        likevegas: bool,
        likebroadway: bool,
        likemusicals: bool,
    ):
        self.userid = userid
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.city = city
        self.state = state
        self.email = email
        self.phone = phone
        self.likesports = likesports
        self.liketheatre = liketheatre
        self.likeconcerts = likeconcerts
        self.likejazz = likejazz
        self.likeclassical = likeclassical
        self.likeopera = likeopera
        self.likerock = likerock
        self.likevegas = likevegas
        self.likebroadway = likebroadway
        self.likemusicals = likemusicals


class Venue(Base):
    __tablename__ = 'venue'

    venueid = sa.Column(sa.SmallInteger, primary_key=True)
    venuename = sa.Column(sa.VARCHAR(100))
    venuecity = sa.Column(sa.VARCHAR(30))
    venuestate = sa.Column(sa.CHAR(2))
    venueseats = sa.Column(sa.Integer)

    __table_args__ = {
        'redshift_sortkey': 'venueid',
        'redshift_distkey': 'venueid',
    }

    def __init__(self, venueid: int, venuename: str, venuecity: str,
                 venuestate: str, venueseats: int):
        self.venueid = venueid
        self.venuename = venuename
        self.venuecity = venuecity
        self.venuestate = venuestate
        self.venueseats = venueseats


class Category(Base):
    __tablename__ = 'category'

    catid = sa.Column(sa.SmallInteger, primary_key=True)
    catgroup = sa.Column(sa.VARCHAR(10))
    catname = sa.Column(sa.VARCHAR(10))
    catdesc = sa.Column(sa.VARCHAR(50))

    __table_args__ = {
        'redshift_sortkey': 'catid',
        'redshift_distkey': 'catid',
    }

    def __init__(self, catid: int, catgroup: str, catname: str, catdesc: str):
        self.catid = catid
        self.catgroup = catgroup
        self.catname = catname
        self.catdesc = catdesc


class Date(Base):
    __tablename__ = 'date'

    dateid = sa.Column(sa.SmallInteger, primary_key=True)
    caldate = sa.Column(sa.Date, nullable=False)
    day = sa.Column(sa.CHAR(3), nullable=False)
    week = sa.Column(sa.SmallInteger, nullable=False)
    month = sa.Column(sa.CHAR(5), nullable=False)
    qtr = sa.Column(sa.CHAR(5), nullable=False)
    year = sa.Column(sa.SmallInteger, nullable=False)
    holiday = sa.Column(sa.Boolean, default=False)

    __table_args__ = {
        'redshift_sortkey': 'dateid',
        'redshift_distkey': 'dateid',
    }

    def __init__(
        self,
        dateid: int,
        caldate: datetime.date,
        day: str,
        week: int,
        month: str,
        qtr: str,
        year: int,
        holiday: bool,
    ):
        self.dateid = dateid
        self.caldate = caldate
        self.day = day
        self.week = week
        self.month = month
        self.qtr = qtr
        self.year = year
        self.holiday = holiday


class Event(Base):
    __tablename__ = 'event'

    eventid = sa.Column(sa.Integer, primary_key=True)
    venueid = sa.Column(sa.SmallInteger, ForeignKey('venue.venueid'))
    catid = sa.Column(sa.SmallInteger, ForeignKey('category.catid'))
    dateid = sa.Column(sa.SmallInteger, ForeignKey('date.dateid'))
    eventname = sa.Column(sa.VARCHAR(200))
    starttime = sa.Column(sa.TIMESTAMP)

    __table_args__ = {
        'redshift_sortkey': 'eventid',
        'redshift_distkey': 'dateid',
    }

    def __init__(self, eventid: int, venueid: int, catid: int, dateid: int,
                 eventname: str, starttime: datetime.datetime):
        self.eventid = eventid
        self.venueid = venueid
        self.catid = catid
        self.dateid = dateid
        self.eventname = eventname
        self.starttime = starttime


class Listing(Base):
    __tablename__ = 'listing'

    listid = sa.Column(sa.Integer, primary_key=True)
    sellerid = sa.Column(sa.Integer, nullable=False)
    eventid = sa.Column(sa.Integer, ForeignKey('event.eventid'))
    dateid = sa.Column(sa.SmallInteger, ForeignKey('date.dateid'))
    numtickets = sa.Column(sa.SmallInteger, nullable=False)
    priceperticket = sa.Column(sa.DECIMAL(8, 2))
    totalprice = sa.Column(sa.DECIMAL(8, 2))
    listtime = sa.Column(sa.TIMESTAMP)

    __table_args__ = {
        'redshift_sortkey': 'listid',
        'redshift_distkey': 'dateid',
    }

    def __init__(
        self,
        listid: int,
        sellerid: int,
        eventid: int,
        dateid: int,
        numtickets: int,
        priceperticket: float,
        totalprice: float,
        listtime: datetime.datetime,
    ):
        self.listid = listid
        self.sellerid = sellerid
        self.eventid = eventid
        self.dateid = dateid
        self.numtickets = numtickets
        self.priceperticket = priceperticket
        self.totalprice = totalprice
        self.listtime = listtime


class Sales(Base):
    __tablename__ = 'sales'

    salesid = sa.Column(sa.Integer, primary_key=True)
    listid = sa.Column(sa.Integer, ForeignKey('listing.listid'))
    sellerid = sa.Column(sa.Integer, nullable=False)
    buyerid = sa.Column(sa.Integer, nullable=False)
    eventid = sa.Column(sa.Integer, ForeignKey('event.eventid'))
    dateid = sa.Column(sa.SmallInteger, ForeignKey('date.dateid'))
    qtysold = sa.Column(sa.SmallInteger, nullable=False)
    pricepaid = sa.Column(sa.DECIMAL(8, 2))
    commission = sa.Column(sa.DECIMAL(8, 2))
    saletime = sa.Column(sa.TIMESTAMP)

    __table_args__ = {
        'redshift_sortkey': 'listid',
        'redshift_distkey': 'dateid',
    }

    def __init__(
        self,
        salesid: int,
        listid: int,
        sellerid: int,
        buyerid: int,
        eventid: int,
        dateid: int,
        qtysold: int,
        pricepaid: float,
        commission: float,
        saletime: datetime.datetime,
    ):
        self.salesid = salesid
        self.listid = listid
        self.sellerid = sellerid
        self.buyerid = buyerid
        self.eventid = eventid
        self.dateid = dateid
        self.qtysold = qtysold
        self.pricepaid = pricepaid
        self.commission = commission
        self.saletime = saletime
