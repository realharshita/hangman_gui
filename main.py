import tkinter as tk
from tkinter import messagebox
import random
import time

root = tk.Tk()
root.title("Hangman Game")
root.geometry("800x600")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True, fill=tk.BOTH)

title_label = tk.Label(frame, text="Hangman Game", font=("Helvetica", 24))
title_label.pack(pady=10)

words = ["PYTHON", "DEVELOPER", "HANGMAN", "COMPUTER", "PROGRAMMING"]
word = random.choice(words)
blanks = ["_"] * len(word)
word_label = tk.Label(frame, text=" ".join(blanks), font=("Helvetica", 18))
word_label.pack(pady=20)

hangman_canvas = tk.Canvas(frame, width=200, height=200, bg="white")
hangman_canvas.pack(pady=20)

hangman_canvas.create_line(50, 150, 150, 150)
hangman_canvas.create_line(100, 150, 100, 50)
hangman_canvas.create_line(100, 50, 150, 50)
hangman_canvas.create_line(150, 50, 150, 70)

input_frame = tk.Frame(frame)
input_frame.pack(pady=20)

letter_label = tk.Label(input_frame, text="Enter a letter: ", font=("Helvetica", 14))
letter_label.grid(row=0, column=0)

letter_entry = tk.Entry(input_frame, font=("Helvetica", 14))
letter_entry.grid(row=0, column=1)

submit_button = tk.Button(input_frame, text="Submit", font=("Helvetica", 14))
submit_button.grid(row=0, column=2, padx=10)

guessed_label = tk.Label(frame, text="Guessed Letters: ", font=("Helvetica", 14))
guessed_label.pack(pady=10)

remaining_label = tk.Label(frame, text="Remaining Guesses: 6", font=("Helvetica", 14))
remaining_label.pack(pady=10)

correct_label = tk.Label(frame, text="Correct Guesses: 0", font=("Helvetica", 14))
correct_label.pack(pady=10)

time_label = tk.Label(frame, text="Time Elapsed: 0s", font=("Helvetica", 14))
time_label.pack(pady=10)

new_game_button = tk.Button(frame, text="New Game", font=("Helvetica", 14))
new_game_button.pack(pady=10)

guessed_letters = []
incorrect_guesses = 0
correct_guesses = 0
max_incorrect_guesses = 6
start_time = time.time()

def update_time():
    elapsed_time = int(time.time() - start_time)
    time_label.config(text=f"Time Elapsed: {elapsed_time}s")
    root.after(1000, update_time)

def update_word_display():
    display_text = " ".join([letter if letter in guessed_letters else "_" for letter in word])
    word_label.config(text=display_text)
    if "_" not in display_text:
        messagebox.showinfo("Congratulations", "You won!")
        reset_game()

def update_hangman_display():
    hangman_canvas.delete("all")
    hangman_canvas.create_line(50, 150, 150, 150)
    hangman_canvas.create_line(100, 150, 100, 50)
    hangman_canvas.create_line(100, 50, 150, 50)
    hangman_canvas.create_line(150, 50, 150, 70)
    if incorrect_guesses >= 1:
        hangman_canvas.create_oval(135, 70, 165, 100)
    if incorrect_guesses >= 2:
        hangman_canvas.create_line(150, 100, 150, 130)
    if incorrect_guesses >= 3:
        hangman_canvas.create_line(150, 110, 130, 100)
    if incorrect_guesses >= 4:
        hangman_canvas.create_line(150, 110, 170, 100)
    if incorrect_guesses >= 5:
        hangman_canvas.create_line(150, 130, 130, 150)
    if incorrect_guesses >= 6:
        hangman_canvas.create_line(150, 130, 170, 150)
    if incorrect_guesses >= 1:
        hangman_canvas.create_oval(140, 80, 145, 85)
        hangman_canvas.create_oval(155, 80, 160, 85)
    if incorrect_guesses >= 2:
        hangman_canvas.create_line(145, 90, 155, 90)

def submit_letter():
    global incorrect_guesses, correct_guesses
    letter = letter_entry.get().upper()
    if len(letter) != 1 or not letter.isalpha():
        messagebox.showwarning("Invalid Input", "Please enter a single letter.")
    elif letter in guessed_letters:
        messagebox.showwarning("Duplicate Guess", "You have already guessed that letter.")
    elif letter in word:
        guessed_letters.append(letter)
        correct_guesses += 1
        update_word_display()
        correct_label.config(text=f"Correct Guesses: {correct_guesses}")
    else:
        incorrect_guesses += 1
        guessed_letters.append(letter)
        update_hangman_display()
        remaining_label.config(text=f"Remaining Guesses: {max_incorrect_guesses - incorrect_guesses}")
        if incorrect_guesses >= max_incorrect_guesses:
            messagebox.showinfo("Game Over", f"You lost! The word was: {word}")
            reset_game()
    letter_entry.delete(0, tk.END)
    guessed_label.config(text="Guessed Letters: " + ", ".join(guessed_letters))

def reset_game():
    global guessed_letters, incorrect_guesses, correct_guesses, word, start_time
    guessed_letters = []
    incorrect_guesses = 0
    correct_guesses = 0
    word = random.choice(words)
    start_time = time.time()
    update_word_display()
    update_hangman_display()
    remaining_label.config(text=f"Remaining Guesses: {max_incorrect_guesses}")
    guessed_label.config(text="Guessed Letters: ")
    correct_label.config(text=f"Correct Guesses: {correct_guesses}")

submit_button.config(command=submit_letter)
new_game_button.config(command=reset_game)

update_time()
root.mainloop()
