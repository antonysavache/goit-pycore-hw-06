from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
    pass

class Phone(Field):
    # реалізація класу
    pass

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    book = {}

    def create_record(self):
        book[self.data.name] = self.data.records

    def read_record(self):
        return book[self.data.name]

    def updete_record(self):
        pass

    def delete_record(self):
        book.pop(data.name)

