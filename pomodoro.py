from tkinter import *
import math
import os
import sys

# ---------------------------- CONSTANTS ------------------------------- #
PINK= "#F72C5B"
RED = "#C62300"
GREEN = "#5CB338"
YELLOW = "#FFF574"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
timer=None
reps=0

# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def bring_app_to_front():
    """Bring the Pomodoro app window to the front of all windows."""
    window.attributes("-topmost", True)  # Make the window topmost
    window.focus_force()  # Force focus on the window
    window.attributes("-topmost", False)  # Reset topmost to allow normal behavior


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps
    window.after_cancel(timer)
    my_label.config(text='Timer')
    checkmark.config(text='')
    canvas.itemconfig(timer_text, text='00:00')
    reps=0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():

    global reps
    reps += 1

    if reps > 8:
        my_label.config(text="Done!", fg=GREEN)
        canvas.itemconfig(timer_text, text='00:00')
        return

    work_sec=WORK_MIN*60
    short_break_sec=SHORT_BREAK_MIN*60
    long_break_sec=LONG_BREAK_MIN*60

    if reps%8==0:
        my_label.config(text="Break",fg=RED)
        count_down(long_break_sec)
    elif reps%2==0:
        my_label.config(text="Break",fg=PINK)
        count_down(short_break_sec)
    else:
        my_label.config(text="Work",fg=GREEN)
        count_down(work_sec)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def count_down(count):

    # python is strongly dynamically typed language as we can change the datatype of any variable dynamically

    count_min=math.floor(count/60)
    count_sec=count%60
    if count_min<10:
        count_min =f'0{count_min}'
    if count_sec<10:
        count_sec =f'0{count_sec}'

    canvas.itemconfig(timer_text,text=f"{count_min}:{count_sec}")
    if count>=0:
        global timer
        timer=window.after(1000,count_down,count-1)

    else:
        marks=''
        work_session=math.floor((reps+1)/2)
        for _ in range(work_session):
            marks += '✔'
            checkmark.config(text=f"{marks}")
        start_timer()
        bring_app_to_front()

# ---------------------------- UI SETUP ------------------------------- #

window=Tk()
window.title('Pomodoro')
window.config(padx=100,pady=50,bg=YELLOW)

#Label
my_label=Label(text="Timer",bg=YELLOW,font=(FONT_NAME,40),fg=GREEN)
my_label.grid(row=0,column=1)

checkmark=Label(bg=YELLOW,font=(FONT_NAME,20),fg=GREEN)
checkmark.grid(row=3,column=1)

#Buttons
start_button = Button(text="Start",command=start_timer)
start_button.config(padx=15,pady=1)
start_button.grid(row=2,column=0)

reset_button = Button(text="Reset",command=reset_timer)
reset_button.config(padx=15,pady=2)
reset_button.grid(row=2,column=2)

#Image
canvas=Canvas(width=200,height=224,bg=YELLOW,highlightthickness=0) #image px resolution
tomato_img= PhotoImage(file=resource_path('tomato.png'))
canvas.create_image(100,112,image=tomato_img)
timer_text= canvas.create_text(100,130,text='00:00',fill='white',font=(FONT_NAME,25,'bold'))
canvas.grid(row=1,column=1)

window.mainloop()