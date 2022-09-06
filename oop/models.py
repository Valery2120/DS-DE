from sqlalchemy import *
from sqlalchemy.orm import create_session, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


class Sex(Base):
    __tablename__ = 'sex'

    sex_id = Column(Integer, primary_key=True)
    sex = Column(String)

    owners = relationship("Owner")

    def __init__(self, sex: str) -> None:
        self.sex = sex


class Nationality(Base):
    __tablename__ = 'nationality'

    nationality_id = Column(Integer, primary_key=True)
    nationality = Column(String)

    owners = relationship("Owner")

    def __init__(self, nationality: str) -> None:
        self.nationality = nationality


association_table = Table('ownership', Base.metadata,
    Column('owner_id', ForeignKey('owner.owner_id'), primary_key=True),
    Column('flat_id', ForeignKey('flat.flat_id'), primary_key=True)
)


class Owner(Base):
    __tablename__ = 'owner'

    owner_id = Column(Integer, primary_key=True)
    last_name = Column(String)
    first_name = Column(String)
    second_name = Column(String)
    day_of_birth = Column(Integer)
    month_of_birth = Column(Integer)
    year_of_birth = Column(Integer)
    sex_id = Column(Integer, ForeignKey('sex.sex_id'))
    nationality_id = Column(Integer, ForeignKey('nationality.nationality_id'))
    phone_number = Column(String)
    email = Column(String)

    flats = relationship(
        "Flat",
        secondary=association_table,
        back_populates="owners")

    def __init__(self, last_name: str, first_name: str, second_name: str, day_of_birth: int, month_of_birth: int, year_of_birth: int) -> None:
        self.last_name = last_name
        self.first_name = first_name
        self.second_name = second_name
        self.day_of_birth = day_of_birth
        self.month_of_birth = month_of_birth
        self.year_of_birth = year_of_birth


class Country(Base):
    __tablename__ = 'country'

    country_id = Column(Integer, primary_key=True)
    country = Column(String)

    regions = relationship("Region")
    passports = relationship("Passport")

    def __init__(self, country: str) -> None:
        self.country = country


class Passport(Base):
    __tablename__ = 'passport'

    passport_id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('owner.owner_id'))
    date_of_issue = Column(String)
    date_of_expiration = Column(String)
    country_id = Column(Integer, ForeignKey('country.country_id'))

    def __init__(self, passport_id: int, date_of_issue: str, date_of_expiration: str) -> None:
        self.passport_id = passport_id
        self.date_of_issue = date_of_issue
        self.date_of_expiration = date_of_expiration


class Region(Base):
    __tablename__ = 'region'

    region_id = Column(Integer, primary_key=True)
    region = Column(String)
    country_id = Column(Integer, ForeignKey('country.country_id'))

    cities = relationship("City")

    def __init__(self, region: str) -> None:
        self.region = region


class City(Base):
    __tablename__ = 'city'

    city_id = Column(Integer, primary_key=True)
    city = Column(String)
    region_id = Column(Integer, ForeignKey('region.region_id'))

    streets = relationship("Street")

    def __init__(self, city: str) -> None:
        self.city = city


class Street(Base):
    __tablename__ = 'street'

    street_id = Column(Integer, primary_key=True)
    street = Column(String)
    city_id = Column(Integer, ForeignKey('city.city_id'))

    def __init__(self, street: str) -> None:
        self.street = street


class Room(Base):
    __tablename__ = 'room'

    room_id = Column(Integer, primary_key=True)
    name = Column(String)
    length = Column(Float)
    width = Column(Float)
    height = Column(Float)
    flat_id = Column(Integer, ForeignKey('flat.flat_id'))

    def __init__(self, name: str, width: int | float, length: int | float, height: int | float) -> None:
        self.name = name
        self.width = width
        self.length = length
        self.height = height


class Flat(Base):
    __tablename__ = 'flat'

    flat_id = Column(Integer, primary_key=True)
    house_number = Column(Integer)
    flat_number = Column(Integer)
    floor = Column(Integer)
    street_id = Column(Integer, ForeignKey('street.street_id'))

    rooms = relationship("Room")
    owners = relationship(
        "Owner",
        secondary=association_table,
        back_populates="flats")

    def __init__(self, house_number: int, flat_number: int, floor: int) -> None:
        self.house_number = house_number
        self.flat_number = flat_number
        self.floor = floor


