from collections import UserDict
import datetime
from book_class import Birthday, Field, Phone, Record, AddressBook, Name



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
    
    return address_book.add_record(rec)


@input_error
def change_command(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"\nNo contact {name} in Adress Book"


@input_error
def exit_command(*args):
    return "\nOkay, I'm going to rest... Get in touch if you need to... See you soon!\n"

@input_error
def hello_command(*args):
    return '\nHello! How can I help you?'


@input_error
def unknown_command(*args):
    return "\nI didn't understand your query, try again..."


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
    return unknown_command, []


@input_error
def main():
    while True:
        user_input = input('\nEnter your request: ').strip()
        
        cmd, data = parser(user_input)
        
        result = f"{cmd(*data) }\n"
        # with open(file_name, 'a+', newline='') as fh:
        #     fh.write((result))
        
        print('\n', result)
        
        if cmd == exit_command:
            break




file_name = "address_book.txt"
expenses = {}
# with open(file_name, "a+") as fh:
#     raw_expenses = fh.readlines()
#     for line in raw_expenses:
#         key, value = line.split("|")
#         expenses[key] = int(value)



if __name__ == "__main__":
    main()