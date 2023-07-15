'''Завдання
У цій домашній роботі ми продовжимо розвивати нашого віртуального асистента з CLI інтерфейсом.

Наш асистент вже вміє взаємодіяти з користувачем за допомогою командного рядка, отримуючи команди та аргументи,
та виконуючи потрібні дії. У цьому завданні потрібно буде попрацювати над внутрішньою логікою асистента, над тим,
як зберігаються дані, які саме дані і що з ними можна зробити.

Застосуємо для цих цілей об'єктно-орієнтоване програмування. Спершу виділимо декілька сутностей (моделей), з якими працюватимемо.

У користувача буде адресна книга або книга контактів. Ця книга контактів містить записи. Кожен запис містить деякий набір полів.

Таким чином ми описали сутності (класи), які необхідно реалізувати. Далі розглянемо вимоги до цих класів та встановимо
їх взаємозв'язок, правила, за якими вони будуть взаємодіяти.

Користувач взаємодіє з книгою контактів, додаючи, видаляючи та редагуючи записи. Також користувач повинен мати можливість
шукати в книзі контактів записи за одним або кількома критеріями (полями).

Про поля також можна сказати, що вони можуть бути обов'язковими (ім'я) та необов'язковими (телефон або email наприклад).
Також записи можуть містити декілька полів одного типу (декілька телефонів наприклад). Користувач повинен мати можливість
додавати/видаляти/редагувати поля у будь-якому записі.

В цій домашній роботі ви повинні реалізувати такі класи:

-+- Клас AddressBook, який наслідується від UserDict, та ми потім додамо логіку пошуку за записами до цього класу.
-+- Клас Record, який відповідає за логіку додавання/видалення/редагування необов'язкових полів та зберігання обов'язкового
    поля Name.
-+- Клас Field, який буде батьківським для всіх полів, у ньому потім реалізуємо логіку, загальну для всіх полів.
-+- Клас Name, обов'язкове поле з ім'ям.
-+- Клас Phone, необов'язкове поле з телефоном та таких один запис (Record) може містити кілька.

Критерії приймання
-- Реалізовано всі класи із завдання.
-- Записи Record в AddressBook зберігаються як значення у словнику. Як ключі використовується значення Record.name.value.
-- Record зберігає об'єкт Name в окремому атрибуті.
-- Record зберігає список об'єктів Phone в окремому атрибуті.
-- Record реалізує методи для додавання/видалення/редагування об'єктів Phone.
-- AddressBook реалізує метод add_record, який додає Record у self.data.'''


from collections import UserDict


class Field:
    def __init__(self, value) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)
        

class Name(Field):
    def __init__(self, value):
        self.value = value
    

class Phone(Field):
    def __init__(self, value):
        self.value = value


class Record:
    def __init__(self, name: Name, phone: Phone = None) -> None:
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
    
    def add_phone(self, phone: Phone):
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
    
    def __str__(self) -> str:
        return f"{self.name}: {', '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record} add success"

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())

address_book = AddressBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Give me name and phone, please"
        except IndexError:
            return "Enter contact name or phone, please"
    return wrapper


@input_error
def add_command(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)
    rec = Record(name, phone)
    return address_book.add_record(rec)


@input_error
def change_command(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"No contact {name} in address book"


@input_error
def exit_command(*args):
    return "Bye...\n"

@input_error
def hello_command(*args):
    return 'How can I help you?'


@input_error
def unknown_command(*args):
    return "I didn't understand your query, try again..."


@input_error
def show_all_command(*args):
    return address_book


COMMANDS = {
            add_command: ("add", "+"),
            change_command: ("change", "зміни"),
            exit_command: ("bye", "exit", "end", "good bye", "close"),
            show_all_command: ("show all", ),
            hello_command: ("hello",)
            }


def parser(text:str):
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                data = text[len(kwd):].strip().split()
                return cmd, data 
    return unknown_command, []


def main():
    while True:
        user_input = input('\nEnter your request: ').strip()
        
        cmd, data = parser(user_input)
        
        result = cmd(*data)
        
        print('\n', result)
        
        if cmd == exit_command:
            break

if __name__ == "__main__":
    main()