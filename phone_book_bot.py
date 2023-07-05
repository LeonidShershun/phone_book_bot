def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "\nEnter user name\n"
        except ValueError:
            return "\nGive me name and phone, please\n"
        except IndexError:
            return "\nEnter contact name\n"
    return wrapper

@input_error
def hello():
    return '\nHow can I help you?\n'


contacts = {}
@input_error
def add_contact(command):
    _, name, phone = command.split(" ", 2)
    contacts[name] = phone
    return f"\nContact {name} added\n"

@input_error
def change_phone(command):
    _, name, phone = command.split(" ", 2)
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return f"\nPhone number changed for contact {name}\n"

@input_error
def show_phone(command):
    _, name = command.split(" ", 1)
    if name not in contacts:
        raise KeyError
    return f"\nPhone number for contact {name}: {contacts[name]}\n"

@input_error
def show_all():
    if not contacts:
        return "\nNo contacts found\n"
    result = "\nContacts:\n"
    for name, phone in contacts.items():
        result += f"\n{name}: {phone}\n"
    return result

def bot():
    print("\nHi! I'm your assistant.\n")



    while True:
        command = input('\nEnter your request:  ').lower()

        if command == "hello":
            print(hello())
        elif command.startswith("add"):
            print(add_contact(command))
        elif command.startswith("change"):
            print(change_phone(command))
        elif command.startswith("phone"):
            print(show_phone(command))
        elif command == "show all":
            print(show_all())
        elif command in ["good bye", "close", "exit"]:
            print("\nGood bye!\n")
            break
        else:
            print("\nI didn't understand your query, try again...\n")

if __name__ == "__main__":
    bot()
