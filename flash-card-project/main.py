# Flash card app for learning French words
# import required modules
from tkinter import *
import pandas as pd
import random
from os.path import exists

# background colour of flashcards app
BACKGROUND_COLOR = "#B1DDC6"

# global variables
random_num = 0

#----------------------- Read CSV Data -----------------------#
# if the user has already learnt some words, then use their saved progress
file_exists = exists("data/words_to_learn.csv")
if file_exists:
    data = pd.read_csv("data/words_to_learn.csv")
    word_dict = data.to_dict(orient="records")
# if user is playing for first time then use all words
else:
    data = pd.read_csv("data/french_words.csv")
    word_dict = data.to_dict(orient="records")


#----------------------- Pick a random French word -----------------------#
# display a random French word from the dictionary of French words on the flashcard canvas
def choose_french_word():
    global random_num, word_dict
    random_num = random.randint(0, len(word_dict))
    french_word = word_dict[random_num]["French"]
    canvas.itemconfig(word, text=french_word)


#----------------------- Flashcard Flip  Functions -----------------------#
# flip the flashcard revealing the english word - changes the flashcard colour and font colour
def flip_card_back():
    global random_num
    english_word = word_dict[random_num]["English"]
    canvas.itemconfig(canvas_image, image=back_card_image)
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word, text=english_word, fill="white")


# if the user knows the French word, remove it from the dict so the flashcards only show unlearnt French words
def known():
    global random_num, word_dict
    # remove known word so it doesn't come up again
    del word_dict[random_num]
    # create df of words that still need to be learnt
    unknown_df = pd.DataFrame(word_dict)
    # create csv of words that still need to be learnt from df
    unknown_df.to_csv("data/words_to_learn.csv", index=False)
    # flip the flashcard back to the French side displaying a new French word
    canvas.itemconfig(canvas_image, image=front_card_image)
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(word, text=choose_french_word(), fill="black")
    window.after(3000, func=flip_card_back)


# if the user didn't know the answer, then flip the flashcard back to a new French word
def unknown():
    # flip the flashcard back to the French side displaying a new French word
    canvas.itemconfig(canvas_image, image=front_card_image)
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(word, text=choose_french_word(), fill="black")
    window.after(3000, func=flip_card_back)


#----------------------- UI Setup -----------------------#
# setup window
window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, background=BACKGROUND_COLOR)
# after 3 seconds display the first word in english
window.after(3000, func=flip_card_back)

# setup canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, background=BACKGROUND_COLOR)
# Load card images
front_card_image = PhotoImage(file="images/card_front.png")
back_card_image = PhotoImage(file="images/card_back.png")
# create flashcard canvas with French side showing first
canvas_image = canvas.create_image(400, 263, image=front_card_image)
language = canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
choose_french_word()
# make the canvas appear on the window
canvas.grid(column=0, row=0, columnspan=2)

# create the wrong button - assign known function
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=unknown)
wrong_button.grid(column=0, row=1)

# create the right button - assign unknown function
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=known)
right_button.grid(column=1, row=1)

# keeps the window open until user closes it
window.mainloop()
