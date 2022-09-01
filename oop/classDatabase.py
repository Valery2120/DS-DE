from sqlalchemy import *
from sqlalchemy.orm import create_session, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


class City(Base):
    __tablename__ = 'city'

    city_id = Column(Integer, primary_key=True)
    city = Column(String)
    region_id = Column(Integer)

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

    def __init__(self, house_number: int, flat_number: int, floor: int) -> None:
        self.house_number = house_number
        self.flat_number = flat_number
        self.floor = floor

if __name__ == '__main__':
    def read_database(session):
        flats = session.query(Flat.flat_id, City.city, Street.street, Flat.house_number,
                              Flat.flat_number, func.round(func.sum(Room.length * Room.width), 2).label('square'))\
            .join(Flat, Room.flat_id == Flat.flat_id)\
            .join(Street, Flat.street_id == Street.street_id)\
            .join(City, Street.city_id == City.city_id).group_by(Flat.flat_id).all()

        for flat in flats:
            if flat[0] <= 10:
                print(f'Площадь квартиры по адресу: {flat[1]}, {flat[2]} str., h.№ {flat[3]}, fl.№ {flat[4]} - {flat[5]} m2')


    engine = create_engine('sqlite:///C://SQLite//property.db', echo=None)
    # Создать транзакцию
    session = create_session(bind=engine)
    read_database(session)
