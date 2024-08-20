# Create a pomodoro timer for work productivity
from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    # stop the timer
    window.after_cancel(timer)
    # reset timer back to 0
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer", fg=GREEN)
    # reset the check marks to zero
    check_label.config(text="")
    global reps
    # reset reps variable to 0
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    # increase reps to keep track of the number of 25-minute work sessions
    global reps
    reps += 1
    # set the work time, and short and long break times using constant variables
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # determine whether it is time for a long or short break, or to continue working.
    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)
        timer_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global reps
    # calculate minute and seconds
    count_min = math.floor(count / 60)
    count_sec = count % 60
    # format seconds correctly when seconds are less than 10
    if count % 60 < 10:
        count_sec = f"0{count_sec}"

    # configure the minute and seconds to the canvas
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        # determine how many rounds the pomodoro timer is on and configure check mark to display completed rounds
        start_timer()
        if reps / 2 == 1:
            check_label.config(text="✓")
        elif reps / 2 == 2:
            check_label.config(text="✓✓")
        elif reps / 2 == 3:
            check_label.config(text="✓✓✓")
        elif reps / 2 == 4:
            check_label.config(text="✓✓✓✓")


# ---------------------------- UI SETUP ------------------------------- #
# configure the window
window = Tk()
window.title("Pomodoro Timer")
window.config(padx=100, pady=50, bg=YELLOW)

# configure the canvas with pomodoro image and timer text
canvas = Canvas(width=200, height=244, bg=YELLOW, highlightbackground=YELLOW)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(102, 112, image=tomato_img)
timer_text = canvas.create_text(102, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# configure initial timer title
timer_label = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 35, "bold"))
timer_label.grid(column=1, row=0)

# configure start button and assign the start_timer function to the command
start_button = Button(text="Start", command=start_timer)
start_button.grid(column=0, row=2)

# configure reset button and assign the reset_timer function to the command
reset_button = Button(text="Reset", command=reset_timer)
reset_button.grid(column=2, row=2)

# configure the check label to keep track of pomodoro rounds
check_label = Label(bg=YELLOW, fg=GREEN, font=(FONT_NAME, 15, "bold"))
check_label.grid(column=1, row=3)

window.mainloop()
