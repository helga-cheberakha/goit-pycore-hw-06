from collections import UserDict

# Implements "Field" to store each field data.
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Validate and store name of the contact record.
class Name(Field):
    def __init__(self, value: str):
        if not value.strip():
            raise ValueError('Name is required and can not be empty.')
         
        super().__init__(value)

# Validate and store phone of the contact record.
class Phone(Field):
    def __init__(self, value: str):
        if not value.isdecimal() or len(value) != 10:
            raise ValueError('Phone number must contain 10 digits.')

        super().__init__(value)

# Handle contact record.
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def find_phone(self, phone: str) -> Phone | None:
        for item in self.phones:
            if item.value == phone:
                return item
    
        return None
    
    def add_phone(self, phone: str) -> None:
        if not self.find_phone(phone):
            self.phones.append(Phone(phone))

    def remove_phone(self, search_phone: str) -> None:
        if phone:= self.find_phone(search_phone):
            self.phones.remove(phone)

    def edit_phone(self, original_phone: str, new_phone: str) -> None:
        if phone:= self.find_phone(original_phone):
            phone.value = Phone(new_phone).value

# Handle address book.
class AddressBook(UserDict):

    def find(self, search_name: str) -> Record | None:
        for name, record in self.items():
            if name.casefold() == search_name.casefold():
                return record
    
        return None

    def add_record(self, record: Record) -> None:
        if not self.find(record.name.value):
            self.data[record.name.value] = record

    def delete(self, removed_name: str) -> None:
        if record:= self.find(removed_name):
            del self.data[record.name.value]


if __name__ == "__main__":
    book = AddressBook()

    # Adds record with name "John" and two phone numbers.
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    book.add_record(john_record)

    # Adds record with name "Jane" and one phone number.
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")

    book.add_record(jane_record)

    # Returns two records: "John" and "Jane"
    for name, record in book.data.items():
        print(record)

    # Try to add duplicate record with a similar name.
    john_duplicate_record = Record("john")
    john_duplicate_record.add_phone("4444444444")

    book.add_record(john_duplicate_record)
    
    # Returns two records: "John" and "Jane"
    for name, record in book.data.items():
        print(record)

    # Adds record with name "Terry" and a wrong phone number.
    terry_record = Record("Terry")
    
    try:
        terry_record.add_phone('123456')
    except ValueError as error:
        print(f'Error: {error}')

    book.add_record(terry_record)

    # Returns three records: "John", "Jane" and "Terry".
    # "Terry" record has empty phone element.
    for name, record in book.data.items():
        print(record)

    # Update phone numbers of the "John" record.
    # Currently "John" record has two phone numbers:
    # - 1234567890
    # - 5555555555
    # New phone numbers will be:
    # - 1234567890
    # - 1112223332
    john = book.find("John")
    john.edit_phone("4444444444", "1112223331")

    try:
        john.edit_phone("5555555555", "111222333")
    except ValueError as error:
        print(f'Error: {error}')

    john.edit_phone("5555555555", "1112223332")
    print(john)

    # Find contact records by their name and
    # find whether they have required phone number.
    jane = book.find("jane")
    jane_found_phone1 = jane.find_phone("9876543210")
    print(f"{jane.name}: {jane_found_phone1}")
    jane_found_phone2 = jane.find_phone("9876543211")
    print(f"{jane.name}: {jane_found_phone2}")

    # Delete contact records.
    book.delete("Jane")
    book.delete("Maria")
    # Returns two records: "John" and "Terry".
    for name, record in book.data.items():
        print(record)
