from models import *

if __name__ == '__main__':
    def request(session):
        flats = session.query(Flat.flat_id, City.city, Street.street, Flat.house_number,
                              Flat.flat_number, func.round(func.sum(Room.length * Room.width),2).label('square'))\
            .join(Flat, Room.flat_id == Flat.flat_id)\
            .join(Street, Flat.street_id == Street.street_id)\
            .join(City, Street.city_id == City.city_id).group_by(Flat.flat_id).all()

        return flats

    def printer(flats):
        for flat in flats:
            if flat[0] <= 10:
                print(f'Площадь квартиры по адресу: {flat[1]}, {flat[2]} str., h.№ {flat[3]}, fl.№ {flat[4]} - {flat[5]} m2')


    engine = create_engine('sqlite:///property.db', echo=None)
    # Создать транзакцию
    session = create_session(bind=engine)
    printer(request(session))