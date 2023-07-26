from collections import UserDict
import datetime
import pickle


class Field:
    def __init__(self, value) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)
        

class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        value = value.replace('/', '-')\
                     .replace('.', '-')
        try:
            self.__value = datetime.datetime.strptime(value, '%d-%m-%Y')
            return self.__value
        except ValueError:
            raise ValueError("\nInvalid date format for Birthday.\n")
        
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)


class Name(Field):
    def __init__(self, value):
        self.value = value
    

class Phone(Field):
    def __init__(self, value):
        self.__phone = None
        self.phone = value

    @property
    def value(self):
        return self.__phone

    @value.setter
    def phone(self, value):
        correct = ("(", ")", "-", " ")
        for i in correct:
            value = value.replace(i, "")
        if len(value) == 13 and value.startswith('+38'):
            self.__phone = value
            return self.__phone
        elif len(value) == 12 and value.startswith('38'):
            self.__phone = f"+{value}"
            return self.__phone
        elif len(value) == 10:
            self.__phone = f"+38{value}"
            return self.__phone
        else:
            raise ValueError("Invalid phone number") 


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None) -> None:
        self.name = name
        self.phones = []
        self.birthday = birthday
        if phone:
            self.phones.append(phone)
    
    def add_phone(self, phone: Phone):
        if phone:
            if phone.value not in [p.value for p in self.phones]:
                self.phones.append(phone)
                return f"Phone {phone} add to contact {self.name}"
            return f"{phone} present in phones of contact {self.name}"
    
    def change_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
                return f"Old phone {old_phone} change to {new_phone}"
        return f"{old_phone} not present in phones of contact {self.name}"
    
    def days_to_birthday(self):
        if self.birthday:
            today = datetime.date.today()
            birthday_day, birthday_month = self.birthday.get_day_month()
            next_birthday = datetime.date(today.year, birthday_day, birthday_month)
            if today > next_birthday:
                next_birthday = datetime.date(today.year + 1, birthday_day, birthday_month)
            days_to_birthday = (next_birthday - today).days
            return days_to_birthday
    
    def __str__(self) -> str:
        return f"{self.name}: {', '.join(str(p) for p in self.phones)}"
    
    __repr__ = __str__

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record} add success"
    
    def search_contacts(self, search_string):
        search_string = search_string.lower()
        results = []
        for record in self.data.values():
            if (search_string in record.name.value.lower())\
                  or any(search_string in phone.value.lower() for phone in record.phones):
                results.append(record)
        return results
    
    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())
    
    def iterator(self, fh_size):
        items = list(self.data.values())
        num_items = len(items)
        start = 0
        while start < num_items:
            end = start + fh_size
            yield items[start:end]
            start = end

    def save_book(self, file_name):
        with open(file_name, 'wb') as fh:
            pickle.dump(self.data, fh)

    def load_book(self, file_name):
        try:
            with open(file_name, 'rb') as fh:
                self.data = pickle.load(fh)
        except FileNotFoundError:
            self.data = {}
    


address_book = AddressBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "\nEnter user name"
        except ValueError:
            return "\nGive me name and phone, please"
        except IndexError:
            return "\nEnter contact name or phone, please"
    return wrapper


@input_error
def add_command(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)
    rec = Record(name, phone)
    address_book.save_book(file_name)
    return address_book.add_record(rec)


@input_error
def change_command(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = address_book.get(str(name))
    if rec:
        rezult = rec.change_phone(old_phone, new_phone)
        address_book.save_book(file_name)
        return rezult
    return f"\nNo contact {name} in Adress Book"


@input_error
def exit_command(*args):
    return "\nOkay, I'm going to rest... Get in touch if you need to... See you soon!\n"

@input_error
def hello_command(*args):
    return '\nHello! How can I help you?'


@input_error
def unknown_command(_text: str):
    for f in  _text.split():
        if f in address_book.keys():
            contact = (str(address_book[f]))
            print(f'\nYou may have searched for this contact "{contact}" by "{f}" in "{_text}"')
        elif f.isdigit():
            for contact in address_book.values():
                if f in str(contact.phones):
                    print(f'\nYou may have searched for this contact "{contact}" by "{f}" in "{_text}"')
    return main()
        

@input_error
def show_all_command(*args):
    if address_book:
        return address_book
    else:
        return "\nNo data in Adress Book..."
    


COMMANDS = {
    add_command: ("add", "+"),
    change_command: ("change", "зміни"),
    exit_command: ("bye", "exit", "end", "good bye", "close"),
    show_all_command: ("show all", ),
    hello_command: ("hello",)  
}


@input_error
def parser(text:str):
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                data = text[len(kwd):].strip().split()
                return cmd, data 
            
                

    return unknown_command, [text]




@input_error
def main(): 
    address_book.load_book(file_name)
    
 
    while True:
        user_input = input('\nEnter your request: ').strip()
        cmd, data = parser(user_input)
        result = cmd(*data)
        if result is not None:
            print(f"\n{result}\n")
        if cmd == exit_command:
            address_book.save_book(file_name)
            break




file_name = "address_book.pickle"


if __name__ == "__main__":
    main()


