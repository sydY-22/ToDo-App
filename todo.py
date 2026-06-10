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



def main():
    test = ToDo()
    test.check_file()
    test.create_todo()


if __name__ == "__main__":
    main()

