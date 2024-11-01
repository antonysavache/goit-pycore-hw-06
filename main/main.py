# main.py
from shared.utils import parse_input
from wrappers import phone_handler, edit_handler
from storage import contacts, leave_commands
from models import Record, Phone, Name

def exit():
    print("Good bye!")

def hello():
    print('How can I help you?')

def add_contact(args):
    if len(args) != 2:
        print("Give me name and phone please")
        return

    name, phone = args
    try:
        if name in contacts.data:
            record = contacts.find(name)
            record.add_phone(phone)
        else:
            record = Record(name)
            record.add_phone(phone)
            contacts.add_record(record)
        print(f"Contact {name} added with phone {phone}")
    except ValueError as e:
        print(f"Error: {e}")

def change_contact(args):
    if len(args) != 2:
        print("Give me name and new phone please")
        return

    name, new_phone = args
    try:
        record = contacts.find(name)
        if not record:
            print(f"Contact {name} not found")
            return

        if record.phones:
            old_phone = record.phones[0].value
            record.edit_phone(old_phone, new_phone)
            print(f"Phone number for {name} changed from {old_phone} to {new_phone}")
        else:
            record.add_phone(new_phone)
            print(f"Added phone {new_phone} to contact {name}")
    except ValueError as e:
        print(f"Error: {e}")

def delete_contact(args):
    if len(args) != 1:
        print("Give me name to delete")
        return

    name = args[0]
    try:
        contacts.delete(name)
        print(f"Contact {name} deleted")
    except KeyError:
        print(f"Contact {name} not found")

def delete_phone(args):
    if len(args) != 2:
        print("Give me name and phone to delete")
        return

    name, phone = args
    try:
        record = contacts.find(name)
        if not record:
            print(f"Contact {name} not found")
            return

        record.remove_phone(phone)
        print(f"Phone {phone} removed from contact {name}")
    except ValueError as e:
        print(f"Error: {e}")

def all():
    if not len(contacts.data):
        print('No Names, no numbers')
    else:
        for record in contacts.data.values():
            print(record)

@phone_handler
def phone(args):
    record = contacts.find(args[0])
    if record and record.phones:
        print('; '.join(str(p) for p in record.phones))

@edit_handler
def edit(args):
    print(f"Contact {args[0]} updated with number {args[1]}")

def show_help():
    commands = {
        "hello": "Show welcome message",
        "add [name] [phone]": "Add new contact",
        "change [name] [new_phone]": "Change contact's phone",
        "phone [name]": "Show contact's phone",
        "all": "Show all contacts",
        "delete [name]": "Delete contact",
        "delete-phone [name] [phone]": "Delete phone from contact",
        "help": "Show this help message",
        "exit/close": "Exit the program"
    }
    print("\nAvailable commands:")
    for cmd, desc in commands.items():
        print(f"{cmd:25} - {desc}")

config = {
    'hello': lambda args: hello(),
    'add': lambda args: add_contact(args),
    'change': lambda args: change_contact(args),
    'delete': lambda args: delete_contact(args),
    'delete-phone': lambda args: delete_phone(args),
    'phone': lambda args: phone(args),
    'all': lambda args: all(),
    'help': lambda args: show_help(),
}

def main():
    print("Welcome to the assistant bot!")
    print("Type 'help' to see available commands")

    while True:
        user_input = input("\nEnter a command: ")
        try:
            command, *args = parse_input(user_input)

            if command in leave_commands:
                exit()
                break

            if command in config:
                config[command](args)
            else:
                print("Invalid command. Type 'help' to see available commands.")

        except ValueError as e:
            print(e)
        except IndexError:
            print("Please provide all required arguments")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()