## Аннотация классов, функций и т.д. только на английском языке. Переведешь. Пример ниже.
## В классе описываешь только то, что он представляет собой.
class Address:
    """
    Class Address stores information about flat address.
    """

## В функции описываешь, что она делает и ее параметры следующим образом, тогда при наведении на функцию ты увидишь это описание.
## При аннотации типизации функций номера чаще всего имеют тип int. Если ты не уверен точно или есть инвариантность ввода различных
## типов, то указываешь так int|float (python 3.10) или Union[int,float] (Python 3.9).
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
        """Печатает адрес квартиры"""
        print(f"{self.street} {self.house}/{self.flat}")

## Функции в описании класса указывать тоже не надо. Они автоматически подтянутся.
class Room:
    """
    Класс для определения площади и объема комнаты

    Методы:
    square()
        Определяет площадь комнаты
    volume()
        Определяет объем комнаты
    """

    def __init__(self, width: float, length: float, height: float) -> None:
        self.width = width
        self.length = length
        self.height = height

    def square(self) -> float:
        return self.width * self.length

    def volume(self) -> float:
        return self.square() * self.height

    def show_room(self) -> None:
        print(f"ширина - {self.width}м, длина - {self.length}м, высота - {self.height}м")

## Если класс не наследует другие, скобки не нужны.
class Flat():
    """
    Класс для определения площади, объема и стоимости квартиры.

    Методы:
    add_room(name, length, width, height):
        Добавляет помещение в квартиру.
    square():
        Определяет площадь квартиры.
    price()
        Определяет стоимость квартиры.
    volume()
        Определяет объем квартиры.
    show_brief()
        Печатает информацию о стоимости, площади и объеме квартиры.
    show_full()
        Печатает информацию:
        адрес,
        стоимость, площадь и объем квартиры,
        название, ширину, длину и высоту комнаты.
    """

    price_per_one_meter = 600
    number = 1

    def __init__(self, street: str, house: str, flat_number: str) -> None:
        self.address = Address(street, house, flat_number)
        self.rooms = {}

    def add_room(self, name: str, width: float, length: float, height: float) -> None:
        """Добавляется помещение в квартиру."""
        if name in self.rooms.keys():
            name = name + '_' + str(self.number)
            self.number += 1
        self.rooms[name] = Room(width, length, height)

    def square(self) -> float:
        """Определяет площадь квартиры."""
        if self.rooms:
            return sum(room.square() for room in self.rooms.values())

    def price(self) -> float:
        """Определяет стоимость квартиры."""
        return self.square() * self.price_per_one_meter

    def volume(self) -> float:
        """Определяет объем квартиры."""
        if self.rooms:
            return sum(room.volume() for room in self.rooms.values())

    def show_brief(self) -> None:
        """Печатает информацию о стоимости, площади и объеме квартиры."""
        self.address.show_address()
        print(f"Стоимость: {self.price():.2f}$, площадь: {self.square():.2f}м2, объем: {self.volume():.2f}м3")

    def show_full(self) -> None:
        """
        Печатает информацию:
        адрес,
        стоимость, площадь и объем квартиры,
        название, ширину, длину и высоту комнаты.
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

    flats = (flat_01, flat_02)

    for flat in flats:
        flat.show_full()
        print()
