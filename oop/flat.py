class Address:
    """
    Class Address stores information about flat address.
    """

    def __init__(self, street: str, house: str, flat: str) -> None:
        """
         Init Addres object with it's parameters.

            :param street: Street name.
            :param house: House number.
            :param flat: Flat number.
        """

        self.street = street
        self.house = house
        self.flat = flat

    def show_address(self) -> None:
        """
        Print the address of the flat.
        """

        print(f"{self.street} {self.house}/{self.flat}")


class Room:
    """
    Сlass calculates square and volume of the flat.
    """

    def __init__(self, width: int | float, length: int | float, height: int | float) -> None:
        """
         Init Room object with it's parameters.

            :param width: Room width
            :param length: Room length
            :param height: Room height
        """

        self.width = width
        self.length = length
        self.height = height

    def square(self) -> float:
        """
        Calculates square of the room.

            :return: square of the room.
        """

        return self.width * self.length

    def volume(self) -> float:
        """
         Calculates volume of the room.
            :return: volume of the room.
         """

        return self.square() * self.height

    def show_room(self) -> None:
        """Print information about width, length and height of the room"""

        print(f"ширина - {self.width}м, длина - {self.length}м, высота - {self.height}м")


## Лучше описывать параметры класса в документации.
class Flat:
    """
    Сlass defines square, volume and price of the flat.
    """

    price_per_one_meter = 600
    number = 1

    def __init__(self, street: str, house: str, flat_number: str) -> None:
        """
        Init Flat object with it's parameters.
            :param street: Street name.
            :param house: House number.
            :param flat_number: Flat number.
        """

        self.address = Address(street, house, flat_number)
        self.rooms = {}

    def add_room(self, name: str, width: float, length: float, height: float) -> None:
        """
        Add the room to the flat
            :param name: Room name.
            :param width: Room width.
            :param length: Room length.
            :param height: Room height.
        """

        if name in self.rooms.keys():
            name = name + '_' + str(self.number)
            self.number += 1
        self.rooms[name] = Room(width, length, height)

    def square(self) -> float:
        """
        Calculates square of the flat
            :return: Square of the flat
        """

        if self.rooms:
            return sum(room.square() for room in self.rooms.values())

    def price(self) -> float:
        """
        Calculates price of the flat
            :return: Price of the flat
        """
        return self.square() * self.price_per_one_meter

    def volume(self) -> float:
        """
        Calculates volume of the flat
            :return: Volume of the flat
        """

        if self.rooms:
            return sum(room.volume() for room in self.rooms.values())

    def show_brief(self) -> None:
        """Print brief information about cost, square and volume of the flat."""

        self.address.show_address()
        print(f"Стоимость: {self.price():.2f}$, площадь: {self.square():.2f}м2, объем: {self.volume():.2f}м3")

    def show_full(self) -> None:
        """
        Print full information about flat:
        address, cost, square and volume of the flat;
        name, width, length and height of the room.
        """

        self.show_brief()

        if self.rooms:
            for name, room in self.rooms.items():
                print(f'{name}:', end=' ')
                room.show_room()


if __name__ == "__main__":

    flat_01 = Flat('Советская', '1', '42')
    flat_01.add_room('Комната', 3., 3.6, 2.5)
    flat_01.add_room('Комната', 2.9, 3.9, 2.5)
    flat_01.add_room('Комната', 1.9, 3.2, 2.5)
    flat_01.add_room('Кухня', 2.3, 1.5, 2.5)
    flat_01.add_room('Туалет', 1., 1.8, 2.5)
    flat_01.add_room('Ванна', 2.1, 1.3, 2.5)

    flat_02 = Flat('Билецкого', '45', '35')
    flat_02.add_room('Комната', 3.7, 2.1, 2.6)
    flat_02.add_room('Кухня', 2.2, 1.7, 2.6)
    flat_02.add_room('Туалет', 1.1, 1.7, 2.6)
    flat_02.add_room('Ванна', 2.3, 1.7, 2.6)

    ## Кортеж неизменяемая последовательность, поэтому, если ты захочешь добавить квартиру, придется создавать новый кортеж.
    ## Здесь лучше использовать список.
    flats = (flat_01, flat_02)

    for flat in flats:
        flat.show_full()
        print()

