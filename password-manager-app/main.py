# import modules
import tkinter
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    # delete previous entry
    password_entry.delete(0, tkinter.END)

    # create list of letters
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    # create list of numbers
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # create list of symbols
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # create variables to hold a random range for letters, symbols, numbers
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    # generate random password by adding random letters, numbers and symbols to a list and then shuffling the list
    password_list = [random.choice(letters) for char in range(nr_letters)]
    password_list += [random.choice(symbols) for symbol in range(nr_symbols)]
    password_list += [random.choice(numbers) for num in range(nr_numbers)]
    random.shuffle(password_list)

    # join the list into a single string
    password = "".join(password_list)
    # display the password in the GUI
    password_entry.insert(0, password)
    # add the password to the user's clipboard
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    # get the website, user and password information
    web = website_entry.get()
    user = user_entry.get()
    password = password_entry.get()
    # save the information into a dictionary
    new_data = {
        web: {
            "email": user,
            "password": password
        }
    }
    # QA for missing info fields
    if len(web) == 0 or len(password) == 0:
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty")
    else:
        # try except block to save the data in json file
        # read current json file
        try:
            with open("data.json", "r") as file:
                # Read old data
                data = json.load(file)

        # if json file doesn't exist then create one with info
        except FileNotFoundError:
            with open("data.json", "w") as file:
                # Saving updated data
                json.dump(new_data, file, indent=4)

        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as file:
                # Saving updated data
                json.dump(data, file, indent=4)
        # remove saved website and password info from GUI fields
        finally:
            website_entry.delete(0, tkinter.END)
            password_entry.delete(0, tkinter.END)


# ---------------------------- Search Website ------------------------------- #
# find saved password for a website
def search_website():
    website_name = website_entry.get()

    # open json file with saved passwords
    try:
        with open("data.json", "r") as data_file:
            # Store data into dict
            website_data = json.load(data_file)

    # if no data is found then print helpful message
    except FileNotFoundError:
        messagebox.showerror(title="Oops", message="No data file found. If you generate a password and press the add "
                                                   "button, a data file will be generated automatically.")
    # get information for specified website
    try:
        website_record = website_data[website_name]

    # print helpful message if website entry doesn't exist
    except KeyError:
        messagebox.showerror(title="Oops", message="No username and password exists for this Website")

    # display website information
    else:
        messagebox.showinfo(title=f"{website_name} information", message=f"Username: {website_record['email']}\n"
                                                                         f"Password: {website_record['password']}")


# ---------------------------- UI SETUP ------------------------------- #
# configure the GUI window
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Create website label, entry and button
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

website_entry = Entry(width=35)
website_entry.focus()
website_entry.grid(column=1, row=1, columnspan=2)

website_button = Button(text="Search", width=15, command=search_website)
website_button.grid(column=3, row=1)

# create user label and entry
user_label = Label(text="Email/Username:")
user_label.grid(column=0, row=2)

user_entry = Entry(width=55)
# add your email into here, so it will appear each time you load up the app
#user_entry.insert(0, "myemail@mail.com")
user_entry.grid(column=1, row=2, columnspan=3)

# create password label, entry and button
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

password_entry = Entry(width=35)
password_entry.grid(column=1, row=3)

password_button = Button(text="Generate Password", width=15, command=generate_password)
password_button.grid(column=3, row=3)

# create add button
add_button = Button(text="Add", width=47, command=save_password)
add_button.grid(column=1, row=4, columnspan=3)

window.mainloop()
