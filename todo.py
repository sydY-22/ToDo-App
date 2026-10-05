from pathlib import Path
import json
import tkinter as tk
from tkinter import messagebox
import os
import base64
import datetime
from datetime import timedelta, datetime
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from apscheduler.schedulers.blocking import BlockingScheduler

RED = "#F7374F"
MAROON = "#88304E"
PURPLE = "#522546"
BLACK_COLOR = "#2C2C2C"

#SCOPES = ['https://googleapis.com']

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

class ToDo(tk.Tk):

    def __init__(self):
        super().__init__()

        # title of app:
        self.title("Welcome to ToDo App!: ")
        self.config(bg=BLACK_COLOR)

        # app icon:
        self.app_icon = tk.PhotoImage(file="images/todo-icon-2.png")
        self.iconphoto(False, self.app_icon)

        # welcome text:
        self.welcome_label = tk.Label(text="Welcome to ToDo App!: ", font=("Helvetica", 35, "bold"), fg=PURPLE, bg=BLACK_COLOR)
        self.welcome_label.grid(column=1, row=0)

        # display list:
        self.listbox = tk.Listbox(self, font=("Helvetica", 12, "bold"), width=50, bg=BLACK_COLOR, fg=RED)
        self.listbox.grid(column=1, row=2, rowspan=1, pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.on_click)

        # add title label and entry:
        self.title_label = tk.Label(text="Add Title: ", font=("Helvetica", 16, "bold"), bg=BLACK_COLOR, fg=PURPLE)
        self.title_label.grid(column=0, row=3, rowspan=1)

        self.title_entry = tk.Entry(width=45)
        self.title_entry.grid(column=1, row=3, columnspan=1, rowspan=1, pady=5) # pady

        # add description label and entry:
        self.description_label = tk.Label(text="Add Description: ", font=("Helvetica", 16, "bold"), bg=BLACK_COLOR, fg=PURPLE)
        self.description_label.grid(column=0, row=4, rowspan=1)

        self.description_entry = tk.Entry(width=45)
        self.description_entry.grid(column=1, row=4, columnspan=1, rowspan=1, pady=5) # pady

        # add title and description for todo button:
        self.add_todo_button = tk.Button(text="Add ToDo!", command=self.create_todo, font=("Helvetica", 14, "bold"), fg=MAROON, bg=PURPLE)
        self.add_todo_button.grid(column=1, row=5, columnspan=1, rowspan=1, pady=5) # pady

        # delete todo button:
        self.delete_button = tk.Button(text="Delete ToDo!", command=self.delete_todo, font=("Helvetica", 14, "bold"), fg=MAROON, bg=PURPLE)
        self.delete_button.grid(column=2, row=6, columnspan=1, rowspan=1, pady=5)

        # delete by 'title' label and entry:
        self.delete_label = tk.Label(self, text="Delete by Title: ", font=("Helvetica", 16, "bold"), bg=BLACK_COLOR, fg=PURPLE)
        self.delete_label.grid(column=0, row=6, columnspan=2, rowspan=1, pady=5, sticky="w")

        self.delete_entry = tk.Entry(self, width=45)
        self.delete_entry.grid(column=1, row=6, columnspan=1, rowspan=1, pady=5)


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
    
    def get_gmail_service(self):
        """Gets the authorized Gmail API service."""
        creds = None

        # stores user's access and refresh tokens
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # no valid credentials let user login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                # save creds for the next run
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
        return build('gmail', 'v1', credentials=creds)

    def show_confirmation(self, todo_text):
        """Display the yes/no message box."""
        response = messagebox.askyesno("Confirmation", 
                                       f"Do you want to set a Reminder for Tomowrrow?: About {todo_text}") 

        if response:
            print("User Clicked Yes!")
            return response
        else:
            print("User Clicked No!")
            return response

    def send_raw_email(self, to_email, subject, body):
        """Creates and sends the email using Gmail API."""
        try:
            service = self.get_gmail_service()

            # build MIME structure
            message = MIMEText(body)
            message['to'] = to_email
            message['subject'] = subject

            # requires base64url encoding of email byte string        
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            create_message = {'raw': raw_message}

            # execute send command
            send_operation = service.users().messages().send(userId="me", body=create_message).execute()
            print(f"Message successfully sent! Message ID: {send_operation["id"]}")

        except HttpError as error:
            print(f"An error occurred: {error}")
    
    def schedule_reminder(self, to_email, subject, body):
        """Schedule a time to send reminder."""
        scheduler = BlockingScheduler()
        current_time = datetime.now()

        tomorrow = current_time + timedelta(days=1)

        print(f"Scheduler active. Email queued for execution at: {tomorrow}!")
        scheduler.add_job(self.send_raw_email, 
                          'date', run_date=tomorrow, kwargs={'to_email': to_email, 'subject': subject, 'body': body})

        # starts execution loop
        scheduler.start()

    def on_click(self, event):
        """Gets the selected item on click."""
        widget = event.widget # get listbox widget emitting the event

        # get clicked item index
        selection = widget.curselection()

        # check if user selected a listbox item
        if selection:
            index = selection[0]
            value = widget.get(index) # get string value
            value_ls = value.split("-")
            subject = f"Reminder!: {value_ls[0]}"
            body = value_ls[1]
            to_email = 'sbabb131@gmail.com'

            print(f"Index: {index} - Value: {value}")

            if self.show_confirmation(value):
                print("Send Reminder!")
                self.send_raw_email(to_email=to_email, subject=subject, body=body)
                # self.schedule_reminder(to_email=to_email, subject=subject, body=body)
                # print(self.get_gmail_service)
            else:
                print("Do NOT send Reminder!")
   

    def menu(self):
        """Display menu options."""
        print("1. List ToDo's")
        print("2. Create ToDo")
        print("3. Delete ToDo")
        print("4. Exit!")



def main():
    test = ToDo()
    test.check_file()
    test.list_todo()
    test.mainloop()

        