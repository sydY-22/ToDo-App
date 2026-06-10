from pathlib import Path
import json

class ToDo:

    def check_file(self):
        """Checks if data exists. if not create data."""
        file_path = Path("todo-list.json")

        if file_path.is_file():
            print("The data exists.")
        else:
            print("The data does NOT exist. Needs to be created.")
            list = {}

            with open("todo-list.json", "w", encoding="utf-8") as data:
                json.dump(list, data, indent=4)
    
    def create_todo(self):
        """Creates the todo."""
        add_title = input("Please enter a title for the todo: ")
        add_description = input("Please enter a description for the todo: ")

        new_todo = {}
        new_todo["Title"] = add_title
        new_todo["Description"] = add_description

        with open("todo-list.json", "r", encoding="utf-8") as data:
            file_json = json.load(data)
        
        total_todos = len(file_json)

        file_json[total_todos+1] = new_todo

        with open("todo-list.json", "w", encoding="utf-8") as data:
            json.dump(file_json, data, indent=4)
        
        print(f"ToDo Added!: {new_todo["Title"]} -  {new_todo['Description']}")
        print()
    
    def list_todo(self):
        """List all todos."""
        print("List of ToDo's: ")

        with open("todo-list.json", "r", encoding="utf-8") as data:
            file_json = json.load(data)
        
        for value in file_json.values():
            print(f"Title: {value["Title"]} - Description: {value["Description"]}")
        
        print()
    
    def delete_todo(self):
        

    def menu(self):
        """Display menu options."""
        print("1. List ToDo's")
        print("2. Create ToDo")
        print("3. Delete ToDo")
        print("4. Exit!")



def main():
    test = ToDo()
    test.check_file()

    while True:
        test.menu()
        prompt = input("Choose between options 1-4: ")

        if prompt == '1':
            test.list_todo()
        elif prompt == '2':
            test.create_todo()
        elif prompt == '3':
            print('delete')
        else:
            False
        
    


if __name__ == "__main__":
    main()

