import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Hangman Game")
root.geometry("800x600")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True, fill=tk.BOTH)

title_label = tk.Label(frame, text="Hangman Game", font=("Helvetica", 24))
title_label.pack(pady=10)

word_label = tk.Label(frame, text="_ _ _ _ _ _", font=("Helvetica", 18))
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

new_game_button = tk.Button(frame, text="New Game", font=("Helvetica", 14))
new_game_button.pack(pady=10)

def submit_letter():
    letter = letter_entry.get().upper()
    messagebox.showinfo("Letter Submitted", f"You guessed: {letter}")
    letter_entry.delete(0, tk.END)

submit_button.config(command=submit_letter)

root.mainloop()
