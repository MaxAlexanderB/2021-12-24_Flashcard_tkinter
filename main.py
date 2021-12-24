from tkinter import *
import pandas
import random

current_card = {}
cards_to_learn = []
BACKGROUND_COLOR = "#B1DDC6"

try:
    cards_to_learn = pandas.read_csv("./data/new words.csv").to_dict(orient="records")
except FileNotFoundError:
    cards_to_learn = pandas.read_csv("./data/french_words.csv").to_dict(orient="records")



#---------Define funtions---------#
def random_french_word():
    #------Import Variables------#
    global card_word
    global card_title
    global current_card
    global canvas_image
    global flip_timer
    #--------Cancel any ongoing timers-------#
    window.after_cancel(flip_timer)

    #--------Select Card--------#
    current_card = random.choice(cards_to_learn)

    #--------Adjust Canvas with current card--------#
    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(card_title, text="French", font=("Arial", 40, "italic"), fill="black")
    canvas.itemconfig(card_word, text=f"{current_card['French']}", font=("Arial", 60, "bold"), fill="black")

    #--------Setup timer--------#
    flip_timer = window.after(3000, func=card_flip)


def card_flip():
    #---------Import variables-----#
    global current_card
    global card_title
    global card_word
    global canvas_image

    #-------Update canvas--------#
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(card_title, text="English", font=("Arial", 40, "italic"), fill="white")
    canvas.itemconfig(card_word, text=f"{current_card['English']}", font=("Arial", 60, "bold"), fill="white")


def remove_current():
    global current_card

    #--------Remove current card from deck--------#
    cards_to_learn.remove(current_card)

    #--------Create new deck with remaining cards-------#
    cards_to_learn_csv = pandas.DataFrame(cards_to_learn)
    cards_to_learn_csv.to_csv("./data/new words.csv", index=False)


def right():
    #--------Only remove card if you got it right--------#
    remove_current()
    random_french_word()



#-------Set up GUI--------#
window = Tk()
window.title("Flashcard App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=card_flip)

#-------Setup Canvas-------#
canvas = Canvas(width=800, height=526, highlightthickness=0)
    #-------locate images--------#
card_back_img = PhotoImage(file="./images/card_back.png")
card_front_img = PhotoImage(file="./images/card_front.png")
right_img = PhotoImage(file="./images/right.png")
wrong_img = PhotoImage(file="./images/wrong.png")
    #--------Setup cards--------#
canvas_image = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(column=0, row=0, columnspan=2)
canvas.configure(bg=BACKGROUND_COLOR)
card_title = canvas.create_text(400, 150, text="French", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="trouve", font=("Arial", 60, "bold")) #stay inside canvas with the text because the canvas is the card
        #--------Setup Buttons-------#
button_right = Button(image=right_img, command=right)
button_right.grid(column=0, row=1)
button_wrong = Button(image=wrong_img, command=random_french_word)
button_wrong.grid(column=1, row=1)

#---------Start App---------#

random_french_word()
window.mainloop()