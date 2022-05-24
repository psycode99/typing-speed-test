#  N/B:  This build is really stable yet

# required imports
from tkinter import *
import random
import math
from tkinter import messagebox

# words to be used for typing exercise
words = [
    {'word': 'Russell was one of the few senators who had remained a bachelor.He never admitted he was lonely'.lower()},
    {'word': 'A programming language is simply a tool.'
             'It is no different from any othertool in your hardware box.'.lower()},
    {'word': 'But then, at some point,he realises that he has embarked on a Sisyphean task and gives up'.lower()},
    {'word': 'The skill that most employers look for when recruiting is the ability to think.'
             'Knowledge is valued in a world where information is hard to come by'.lower()},
    {'word': 'So if you are not on our course then find your own. '
             'There is plenty of Facebook groups dedicated to those who are learning to code.'.lower()},
    {'word': 'Do not run out and buy your cone-shaped bras just yet. What I mean is programming will keep evolving.'
             ' In order to stay relevant, you have to keep re-inventing yourself.'.lower()},
    {'word': 'In a company, people tend to complain that the programmers are always playing foosball '
             'or doing something else that does not look like work. '.lower()},
    {'word': 'When you see them enjoying their foosball game, laughing and joking,they are probably suffering inside.'
             'For there is a bug, there is always a bug.'.lower()},
    {'word': 'So you have an awesome app idea. But it is way way way too complicated for your current skill level.'
             'What do you do? You join the Chunking Express.'.lower()},
    {'word': 'Nope, I am not talking about the art house movie.'
             'I am talking about breaking down your programming problem.'.lower()},

]

window = Tk()
window.title('Py Typer')
window.config(bg='#F5F5F5')

minute = 0
second = 0


def reset():
    """
    not yet completed, but its functionality is to allow
    users reset the app, clear the previous text boxes, give a new text,
    and reset the timer. In this build I haven't added the code for resetting
    the timer yet.
    :return:
    """
    reset_word = random.choice(words)  # selects a new random word
    word_box.configure(state='normal')  # changes the state of the word display box from being disabled as i had set
    # in line 154 to being normal so we can edit it
    word_box.delete('1.0', 'end')  # after changing the state to normal we now delete its current content
    word_box.insert(END, reset_word['word'])  # we insert the random word we selected from line 46 above into the now
    # blank word box
    word_box.configure(state='disabled')  # then we change the state back to disabled to prevent the user from editing
    #  its contents

    entry_box.delete('1.0', 'end')  # here we simply delete the content of the entry box

    # this is the part to reset the timer that I haven't included in this build
    timer.config(text=f'Timer: 00:00')
    entry_box.bind('<FocusIn>', start_timer)


def start_timer(event):
    """
    this function calls the countdown function
    when it is being triggered in line 198 by the bind function of the entry_box text widget

    :param event:
    :return:
    """
    count_down(120)  # 120 is 2 minutes converted to seconds and served to the countdown function
    return event


def count_down(count):
    """
    this function is responsible for the countdown functionality
    of the timer
    :param count:
    :return:
    """
    # I currently don't have an explanation for why I did this. Just let it be
    global minute
    global second

    count_min = math.floor(count / 60)  # convert the count param which will be in seconds to minutes
    #  by dividing it by 60 and using math.floor() to get the upper value

    count_sec = count % 60  # convert the count param to real seconds by finding its modulo
    minute = count_min
    second = count_sec
    timer.config(text=f'Timer: {count_min}:{count_sec}')  # change the timer label text to the current min and sec

    #  checks if the count param is greater than 0
    if count > 0:
        window.after(1000, count_down, count - 1)  # after 1000ms i.e = 1 sec. the countdown function is called
        #  and the count param is reduced by 1 until it gets to 0

    #  just a User interface thing
    if count_sec < 10 or count_sec == 0:
        timer.config(text=f'Timer: {count_min}:0{count_sec}')


def calc():
    """
    this function does the majority of the calculations
    for word per min and accuracy
    :return:
    """

    #  like I said earlier I don't know why i did this, but let it be.
    global minute
    global second

    # word_per_min calculation
    original_words = word_box.get('1.0', 'end-1c')  # grabs the current contents of the word_box text widget
    words_typed = entry_box.get('1.0', 'end-1c')[:len(original_words)]  # grabs the current contents of the entry_box
    # text widget from the beginning to end of the length of the original_words. Reason was because I don't want to
    # include parts outside original length in WPM and accuracy calculation for words typed. This could present a bug
    # though, but I'll fix it in future builds

    # converting seconds to minute calculation to use for WPM calculation
    sec_2_min = second / 60
    sec_2_min = minute + sec_2_min
    sec_2_min = 2 - sec_2_min  # subtracting the minute used from the starting minute which 2
    time_used = round(sec_2_min, 2)

    # Actual WPM calculation. WPM formula = (total no. of words / 5) / time_used_in_minutes
    word_len = len(words_typed)
    wpm_init = word_len / 5
    wpm_fin = round(wpm_init / time_used, 2)
    word_per_min = str(wpm_fin)
    wpm.config(text=f'WPM: {word_per_min}')

    # accuracy calculation
    unwanted_chars = [' ', ',', '.', '-']  # list of unwanted characters in word_box & entry_box text

    #  removing these unwanted characters from the original_words and words_typed
    for chars in unwanted_chars:
        if chars in original_words or chars in words_typed:
            original_words = original_words.replace(chars, '')
            words_typed = words_typed.replace(chars, '')

    original_words_len = len(original_words)
    typed_word_len = 0  # point tracker for accuracy

    # pattern for accuracy calculation
    for x in range(len(original_words)):
        try:
            if words_typed[x] == original_words[x]:
                typed_word_len += 1
            elif words_typed[x] != original_words[x]:
                if words_typed[x] == original_words[x + 1]:
                    typed_word_len += 1
        except IndexError:
            pass

    accur = round((typed_word_len / original_words_len) * 100, 2)
    accur = str(accur)
    accuracy.config(text=f'Accuracy: {accur}%')

    messagebox.showinfo('Score', f"Your Word Per Minute (WPM): {word_per_min}\n"
                                 f"Your Accuracy: {accur}%")


title = Label(
    text='Typing Test',
    font=('Arial', 18)
)
title.grid(row=0, column=1)

timer = Label(
    text=f'Timer: 00:00',
    font=('Arial', 11)
)
timer.grid(row=0, column=0)

text = Label(
    text="Let's test your typing speed and accuracy in 2 minutes!!",
    font=('Arial', 11)
)
text.grid(row=1, column=1)

word_box = Text(
                height=10,
                width=52,
                font=("Helvetica", 15),
                wrap='word',
                padx=10,
                pady=10,
                cursor='arrow'
)
word_box.grid(row=2, column=1)

chosen_word = random.choice(words)

word_box.insert(END, chosen_word['word'])
word_box.configure(state='disabled')

entry_box = Text(
                 height=10,
                 width=52,
                 wrap='word',
                 relief='sunken',
                 padx=10,
                 pady=10,
                 bd=1
)
entry_box.grid(row=3, column=1)

submit = Button(
    text='Submit',
    command=calc
)
submit.grid(row=4, column=1)

reset_but = Button(
    text='Reset',
    command=reset
)
reset_but.grid(row=5, column=1)
reset_but.config(width=20)

wpm = Label(text=f'WPM: {str(0.0)}')
wpm.grid(row=6, column=0)

accuracy = Label(text=f'Accuracy: {str(0.0)}%')
accuracy.grid(row=6, column=2)

entry_box.bind('<FocusIn>', start_timer)  # when the entry_box textbox is focused on the start_timer() func will be
# activated
window.mainloop()
