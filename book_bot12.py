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