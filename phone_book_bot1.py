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


contacts = {}


@input_error
def process_command(command, *args):
    if command == "hello":
        print('\nHow can I help you?\n')

    elif command == "add":
        name, phone = args
        contacts[name] = phone
        print(f"\nContact '{name}' added with phone {phone}\n")

    elif command == "change":
        name, phone = args
        if name in contacts:
            contacts[name] = phone
            print(f"\nPhone number changed for contact '{name}'\n")
        else:
            raise KeyError
        
    elif command == "phone":
        name = args[0]
        if name not in contacts:
            raise KeyError
        print(f"\nPhone number for contact '{name}' : {contacts[name]}\n")

    elif command == "show all": 
                if not contacts:
                    print("\nNo contacts found\n")
                result = "\nContacts:\n"
                for name, phone in contacts.items():
                    result += f"\n{name} ==>> {phone}"
                print(result)
                
    elif command == "good bye" or command == "close" or command == "exit":
        print('\nGood bye!\n')
        return True
    
    else:
        print("\nI didn't understand your query, try again...\n")


def parse_command(command):
    parts = command.lower().split(maxsplit=2)
    
    if len(parts) == 1:
        return parts[0], None
    
    elif len(parts) == 2:
        return parts[0], str(parts[1]).capitalize()
    
    elif len(parts) == 3:
        return parts[0], str(parts[1]).capitalize(), parts[2]
    
    else:
        return None



@input_error
def main():
    while True:
        command_save = input('\nEnter your request: ')
        command, *args = parse_command(command_save)

        if process_command(command, *args):
            break


if __name__ == "__main__":
    main()
