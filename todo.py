from pathlib import Path
import json
import tkinter as tk
from tkinter import messagebox

RED = "#F7374F"
MAROON = "#88304E"
PURPLE = "#522546"
BLACK_COLOR = "#2C2C2C"

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

        new_todo = {}
        new_todo["Title"] = self.title_entry.get()
        new_todo["Description"] = self.description_entry.get()

        with open("todo-list.json", "r", encoding="utf-8") as data:
            file_json = json.load(data)
        
        if file_json:
            total_todos = int(next(reversed(file_json))) # gets the last id value
            file_json[total_todos+1] = new_todo   
        else:
            # Calculate the next ID dynamically
            next_id = str(max([int(k) for k in file_json.keys()] + [0]) + 1)
            # Assign the new todo
            file_json[next_id] = new_todo

        self.listbox.insert(tk.END, f"• {new_todo["Title"]} - {new_todo["Description"]}")
        print(f"ToDo Added!: {new_todo["Title"]} -  {new_todo["Description"]}")
        self.title_entry.delete(0, tk.END) # clears the entry field
        self.description_entry.delete(0, tk.END)       

        with open("todo-list.json", "w", encoding="utf-8") as data:
            json.dump(file_json, data, indent=4) 

        print()
    
    def list_todo(self):
        """List all todos."""
        print("List of ToDo's...")

        with open("todo-list.json", "r", encoding="utf-8") as data:
            file_json = json.load(data)
        
        for value in file_json.values():
            self.listbox.insert(tk.END, f"• {value["Title"]} - {value["Description"]}")
            print(f"Title: {value["Title"]} - Description: {value["Description"]}")
        
        print()
    
    def delete_todo(self):
        """Delete a todo from the list."""

        remove_todo = self.delete_entry.get()
        all_items = self.listbox.get(0, tk.END)

        with open("todo-list.json", "r", encoding="utf-8") as data:
            file_json = json.load(data)
        
        todos = list(file_json.values())
        title_todos_ls = [i["Title"] for i in todos]

        if remove_todo not in title_todos_ls:
            return print(f"{remove_todo} NOT in todo list!")
        else:
            for k, v in list(file_json.items()):
                if v["Title"] == remove_todo:
                    print(f"Deleting: {file_json[k]}")
                    index = all_items.index(f"• {file_json[k]["Title"]} - {file_json[k]["Description"]}")
                    self.listbox.delete(index)
                    del file_json[k]

            with open("todo-list.json", "w", encoding="utf-8") as data:
                json.dump(file_json, data, indent=4)
            
        self.delete_entry.delete(0, tk.END) # clears the entry field
        print()

    def menu(self):
        """Display menu options."""
        print("1. List ToDo's")
        print("2. Create ToDo")
        print("3. Delete ToDo")
        print("4. Exit!")
    
    window = tk.Tk()
    window.title("Welcome to ToDo App!: ")
    window.config(bg=BLACK_COLOR)

     # display list:
    listbox = tk.Listbox(window, font=("Helvetica", 12, "bold"), width=50, bg=BLACK_COLOR, fg=RED)
    listbox.grid(column=1, row=2, rowspan=1, pady=5)

    # add title label and entry:
    title_label = tk.Label(text="Add Title: ", font=("Helvetica", 16, "bold"), bg=BLACK_COLOR, fg=PURPLE)
    title_label.grid(column=0, row=3, rowspan=1)

    title_entry = tk.Entry(width=45)
    title_entry.grid(column=1, row=3, columnspan=1, rowspan=1, pady=5) # pady

    # add description label and entry:
    description_label = tk.Label(text="Add Description: ", font=("Helvetica", 16, "bold"), bg=BLACK_COLOR, fg=PURPLE)
    description_label.grid(column=0, row=4, rowspan=1)

    description_entry = tk.Entry(width=45)
    description_entry.grid(column=1, row=4, columnspan=1, rowspan=1, pady=5) # pady

    # delete by 'title' label and entry:
    delete_label = tk.Label(window, text="Delete by Title: ", font=("Helvetica", 16, "bold"), bg=BLACK_COLOR, fg=PURPLE)
    delete_label.grid(column=0, row=6, columnspan=2, rowspan=1, pady=5, sticky="w")

    delete_entry = tk.Entry(window, width=45)
    delete_entry.grid(column=1, row=6, columnspan=1, rowspan=1, pady=5)




def main():
    test = ToDo()
    test.check_file()

    app_icon = tk.PhotoImage(file="todo-icon-2.png")
    test.window.iconphoto(False, app_icon)

    # welcome text:
    welcome_label = tk.Label(text="Welcome to ToDo App!: ", font=("Helvetica", 35, "bold"), fg=PURPLE, bg=BLACK_COLOR)
    welcome_label.grid(column=1, row=0)

    test.list_todo()

    # add title and description for todo button:
    add_todo_button = tk.Button(text="Add ToDo!", command=test.create_todo, font=("Helvetica", 14, "bold"), fg=MAROON, bg=PURPLE)
    add_todo_button.grid(column=1, row=5, columnspan=1, rowspan=1, pady=5) # pady

    # delete todo button:
    delete_button = tk.Button(text="Delete ToDo!", command=test.delete_todo, font=("Helvetica", 14, "bold"), fg=MAROON, bg=PURPLE)
    delete_button.grid(column=2, row=6, columnspan=1, rowspan=1, pady=5)

    test.window.mainloop()

        

