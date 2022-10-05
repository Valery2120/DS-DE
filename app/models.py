from __main__ import db


class Sex(db.Model):
    __tablename__ = 'sex'

    sex_id = db.Column(db.Integer, primary_key=True)
    sex = db.Column(db.String)

    owners = db.relationship("Owner", backref='owners')

    def __init__(self, sex: str) -> None:
        self.sex = sex


class Nationality(db.Model):
    __tablename__ = 'nationality'

    nationality_id = db.Column(db.Integer, primary_key=True)
    nationality = db.Column(db.String)

    # owners = db.relationship("Owner")

    def __init__(self, nationality: str) -> None:
        self.nationality = nationality


association_table = db.Table('ownership', db.Model.metadata,
                             db.Column('owner_id', db.ForeignKey('owner.owner_id'), primary_key=True),
                             db.Column('flat_id', db.ForeignKey('flat.flat_id'), primary_key=True)
                             )


class Owner(db.Model):
    __tablename__ = 'owner'

    owner_id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String)
    first_name = db.Column(db.String)
    second_name = db.Column(db.String)
    day_of_birth = db.Column(db.Integer)
    month_of_birth = db.Column(db.Integer)
    year_of_birth = db.Column(db.Integer)
    sex_id = db.Column(db.Integer, db.ForeignKey('sex.sex_id'))
    nationality_id = db.Column(db.Integer, db.ForeignKey('nationality.nationality_id'))
    phone_number = db.Column(db.String)
    email = db.Column(db.String)

    flats = db.relationship(
        "Flat",
        secondary=association_table,
        back_populates="owners")

    def __init__(self, last_name: str, first_name: str, second_name: str,
                 day_of_birth: int, month_of_birth: int, year_of_birth: int) -> None:
        self.last_name = last_name
        self.first_name = first_name
        self.second_name = second_name
        self.day_of_birth = day_of_birth
        self.month_of_birth = month_of_birth
        self.year_of_birth = year_of_birth


class Country(db.Model):
    __tablename__ = 'country'

    country_id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String)

    regions = db.relationship("Region")
    passports = db.relationship("Passport")

    def __init__(self, country: str) -> None:
        self.country = country


class Passport(db.Model):
    __tablename__ = 'passport'

    passport_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.owner_id'))
    date_of_issue = db.Column(db.String)
    date_of_expiration = db.Column(db.String)
    country_id = db.Column(db.Integer, db.ForeignKey('country.country_id'))

    def __init__(self, passport_id: int, date_of_issue: str, date_of_expiration: str) -> None:
        self.passport_id = passport_id
        self.date_of_issue = date_of_issue
        self.date_of_expiration = date_of_expiration


class Region(db.Model):
    __tablename__ = 'region'

    region_id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String)
    country_id = db.Column(db.Integer, db.ForeignKey('country.country_id'))

    cities = db.relationship("City")

    def __init__(self, region: str) -> None:
        self.region = region


class City(db.Model):
    __tablename__ = 'city'

    city_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String)
    region_id = db.Column(db.Integer, db.ForeignKey('region.region_id'))

    streets = db.relationship("Street")

    def __init__(self, city: str) -> None:
        self.city = city


class Street(db.Model):
    __tablename__ = 'street'

    street_id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String)
    city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'))

    def __init__(self, street: str) -> None:
        self.street = street


class Room(db.Model):
    __tablename__ = 'room'

    room_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    length = db.Column(db.Float)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    flat_id = db.Column(db.Integer, db.ForeignKey('flat.flat_id'))

    def __init__(self, name: str, width: int | float, length: int | float, height: int | float) -> None:
        self.name = name
        self.width = width
        self.length = length
        self.height = height


class Flat(db.Model):
    __tablename__ = 'flat'

    flat_id = db.Column(db.Integer, primary_key=True)
    house_number = db.Column(db.Integer)
    flat_number = db.Column(db.Integer)
    floor = db.Column(db.Integer)
    street_id = db.Column(db.Integer, db.ForeignKey('street.street_id'))

    rooms = db.relationship("Room")
    owners = db.relationship(
        "Owner",
        secondary=association_table,
        back_populates="flats")

    def __init__(self, house_number: int, flat_number: int, floor: int) -> None:
        self.house_number = house_number
        self.flat_number = flat_number
        self.floor = floor
