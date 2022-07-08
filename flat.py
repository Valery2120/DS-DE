class Address:
    def __init__(self, street, house, flat):
        self.street = street
        self.house = house
        self.flat = flat

    def show_address(self):
        print(f"{self.street} {self.house}/{self.flat}")


class Room:
    def __init__(self, width, length, height):
        self.width = width
        self.length = length
        self.height = height

    def square(self):
        return self.width * self.length

    def volume(self):
        return self.square() * self.height

    def show_room(self):
        print(f"ширина - {self.width}м, длина - {self.length}м, высота - {self.height}м")


class Flat(Address):
    price_per_one_meter = 600

    def __init__(self, street, house, flat_number):
        self.address = Address(street, house, flat_number)
        self.rooms = {}

    def add_room(self, name, width, length, height):
        self.rooms[name] = Room(width, length, height)

    def square(self):
        if self.rooms:
            return sum(room.square() for room in self.rooms.values())

    def price(self):
        return self.square() * self.price_per_one_meter

    def volume(self):
        if self.rooms:
            return sum(room.volume() for room in self.rooms.values())

    def show_brief(self):
        self.address.show_address()
        print(f"Стоимость: {self.price():.2f}$, площадь: {self.square():.2f}м2, объем: {self.volume():.2f}м3")

    def show_full(self):
        self.show_brief()

        if self.rooms:
            for name, room in self.rooms.items():
                print(f'{name}:', end=' ')
                room.show_room()


if __name__ == "__main__":


    flat_01 = Flat('Советская', '1', '42')
    flat_01.add_room('Комната', 3., 3.6, 2.5)
    flat_01.add_room('Комната', 2.9, 3.9, 2.5)
    flat_01.add_room('Кухня', 2.3, 1.5, 2.5)
    flat_01.add_room('Туалет', 1., 1.8, 2.5)
    flat_01.add_room('Ванна', 2.1, 1.3, 2.5)

    flat_02 = Flat('Билецкого', '45', '35')
    flat_02.add_room('Комната', 3.7, 2.1, 2.6)
    flat_02.add_room('Кухня', 2.2, 1.7, 2.6)
    flat_02.add_room('Туалет', 1.1, 1.7, 2.6)
    flat_02.add_room('Ванна', 2.3, 1.7, 2.6)

    flats = (flat_01, flat_02)

    for flat in flats:
        flat.show_full()
        print()