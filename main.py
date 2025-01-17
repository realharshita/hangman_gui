import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time
import json
import os

root = tk.Tk()
root.title("Hangman Game")
root.geometry("800x600")

light_theme = {
    "bg": "white",
    "fg": "black",
    "canvas_bg": "white",
    "button_bg": "#f0f0f0",
    "button_fg": "black",
}

dark_theme = {
    "bg": "#121212",
    "fg": "white",
    "canvas_bg": "#212121",
    "button_bg": "#333333",
    "button_fg": "white",
}

current_theme = light_theme

def toggle_theme():
    global current_theme
    if current_theme == light_theme:
        current_theme = dark_theme
    else:
        current_theme = light_theme
    apply_theme()

def apply_theme():
    root.configure(bg=current_theme["bg"])
    for widget in root.winfo_children():
        widget.configure(bg=current_theme["bg"], fg=current_theme["fg"])
    hangman_canvas.configure(bg=current_theme["canvas_bg"])
    submit_button.configure(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    new_game_button.configure(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    hint_button.configure(bg=current_theme["button_bg"], fg=current_theme["button_fg"])

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True, fill=tk.BOTH)

title_label = tk.Label(frame, text="Hangman Game", font=("Helvetica", 24))
title_label.pack(pady=10)

categories = {
    "Programming Languages": ["PYTHON", "JAVA", "RUBY", "PHP", "JAVASCRIPT"],
    "Animals": ["ELEPHANT", "TIGER", "ZEBRA", "PENGUIN", "GIRAFFE"],
    "Countries": ["INDIA", "CANADA", "BRAZIL", "JAPAN", "RUSSIA"],
}
current_category = ""
words = []

def choose_word():
    global words, current_category
    current_category = random.choice(list(categories.keys()))
    words = categories[current_category]
    return random.choice(words)

word = choose_word()
blanks = ["_"] * len(word)
word_label = tk.Label(frame, text=" ".join(blanks), font=("Helvetica", 18))
word_label.pack(pady=20)

category_label = tk.Label(frame, text=f"Category: {current_category}", font=("Helvetica", 14))
category_label.pack()

hangman_canvas = tk.Canvas(frame, width=200, height=200, bg=current_theme["canvas_bg"])
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

submit_button = tk.Button(input_frame, text="Submit", font=("Helvetica", 14), bg=current_theme["button_bg"], fg=current_theme["button_fg"])
submit_button.grid(row=0, column=2, padx=10)

hint_button = tk.Button(input_frame, text="Hint", font=("Helvetica", 14), bg=current_theme["button_bg"], fg=current_theme["button_fg"], command=use_hint)
hint_button.grid(row=0, column=3, padx=10)

guessed_label = tk.Label(frame, text="Guessed Letters: ", font=("Helvetica", 14))
guessed_label.pack(pady=10)

remaining_label = tk.Label(frame, text="Remaining Guesses: 6", font=("Helvetica", 14))
remaining_label.pack(pady=10)

correct_label = tk.Label(frame, text="Correct Guesses: 0", font=("Helvetica", 14))
correct_label.pack(pady=10)

hint_label = tk.Label(frame, text="Hints Remaining: 3", font=("Helvetica", 14))
hint_label.pack(pady=10)

time_label = tk.Label(frame, text="Time Elapsed: 0s", font=("Helvetica", 14))
time_label.pack(pady=10)

new_game_button = tk.Button(frame, text="New Game", font=("Helvetica", 14), bg=current_theme["button_bg"], fg=current_theme["button_fg"], command=lambda: reset_game(True))
new_game_button.pack(pady=10)

menu = tk.Menu(root)
root.config(menu=menu)
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New Game", command=lambda: reset_game(True))
file_menu.add_command(label="Save Game", command=save_game)
file_menu.add_command(label="Load Game", command=load_game)
file_menu.add_command(label="High Scores", command=display_high_scores)
file_menu.add_command(label="Set Custom Words", command=set_custom_words)
file_menu.add_command(label="Exit", command=root.quit)

help_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="How to Play", command=show_instructions)

theme_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Theme", menu=theme_menu)
theme_menu.add_command(label="Toggle Theme", command=toggle_theme)

difficulty_levels = {
    "Easy": 8,
    "Medium": 6,
    "Hard": 4,
}
current_difficulty = "Medium"
max_incorrect_guesses = difficulty_levels[current_difficulty]
hints_remaining = 3

def set_difficulty():
    global current_difficulty, max_incorrect_guesses
    current_difficulty = simpledialog.askstring("Set Difficulty", "Choose difficulty (Easy, Medium, Hard):")
    if current_difficulty not in difficulty_levels:
        current_difficulty = "Medium"
    max_incorrect_guesses = difficulty_levels[current_difficulty]
    remaining_label.config(text=f"Remaining Guesses: {max_incorrect_guesses}")
    reset_game(False)

def set_custom_words():
    global categories
    new_words = simpledialog.askstring("Custom Words", "Enter custom words separated by commas:")
    if new_words:
        custom_words = [word.strip().upper() for word in new_words.split(",")]
        categories["Custom Words"] = custom_words
    reset_game(False)

guessed_letters = []
incorrect_guesses = 0
correct_guesses = 0
start_time = 0
game_start_time = 0
high_scores = []

def update_time():
    global start_time
    if start_time:
        elapsed_time = int(time.time() - start_time)
        time_label.config(text=f"Time Elapsed: {elapsed_time}s")
    root.after(1000, update_time)

def update_word_display():
    display_text = " ".join([letter if letter in guessed_letters else "_" for letter in word])
    word_label.config(text=display_text)
    if "_" not in display_text:
        elapsed_time = int(time.time() - game_start_time)
        save_high_score(elapsed_time)
        show_game_over_stats(True)

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
        correct_label.config(text=f"Correct Guesses: {correct_guesses}")
        update_word_display()
    else:
        guessed_letters.append(letter)
        incorrect_guesses += 1
        remaining_label.config(text=f"Remaining Guesses: {max_incorrect_guesses - incorrect_guesses}")
        update_hangman_display()
        if incorrect_guesses >= max_incorrect_guesses:
            show_game_over_stats(False)
    letter_entry.delete(0, tk.END)
    guessed_label.config(text="Guessed Letters: " + ", ".join(guessed_letters))

submit_button.config(command=submit_letter)

def reset_game(new_game):
    global word, blanks, guessed_letters, incorrect_guesses, correct_guesses, start_time, game_start_time, hints_remaining
    if new_game:
        set_difficulty()
    word = choose_word()
    blanks = ["_"] * len(word)
    word_label.config(text=" ".join(blanks))
    guessed_letters = []
    incorrect_guesses = 0
    correct_guesses = 0
    start_time = time.time()
    game_start_time = time.time()
    hints_remaining = 3
    remaining_label.config(text=f"Remaining Guesses: {max_incorrect_guesses}")
    guessed_label.config(text="Guessed Letters: ")
    correct_label.config(text=f"Correct Guesses: {correct_guesses}")
    time_label.config(text="Time Elapsed: 0s")
    hint_label.config(text=f"Hints Remaining: {hints_remaining}")
    update_hangman_display()

def save_game():
    game_state = {
        "word": word,
        "guessed_letters": guessed_letters,
        "incorrect_guesses": incorrect_guesses,
        "correct_guesses": correct_guesses,
        "game_start_time": game_start_time,
        "start_time": start_time,
        "hints_remaining": hints_remaining,
    }
    with open("hangman_save.json", "w") as f:
        json.dump(game_state, f)
    messagebox.showinfo("Game Saved", "Game saved successfully.")

def load_game():
    global word, guessed_letters, incorrect_guesses, correct_guesses, start_time, game_start_time, hints_remaining
    if os.path.exists("hangman_save.json"):
        with open("hangman_save.json", "r") as f:
            game_state = json.load(f)
        word = game_state["word"]
        guessed_letters = game_state["guessed_letters"]
        incorrect_guesses = game_state["incorrect_guesses"]
        correct_guesses = game_state["correct_guesses"]
        game_start_time = game_state["game_start_time"]
        start_time = game_state["start_time"]
        hints_remaining = game_state["hints_remaining"]
        update_word_display()
        update_hangman_display()
        remaining_label.config(text=f"Remaining Guesses: {max_incorrect_guesses - incorrect_guesses}")
        guessed_label.config(text="Guessed Letters: " + ", ".join(guessed_letters))
        correct_label.config(text=f"Correct Guesses: {correct_guesses}")
        elapsed_time = int(time.time() - game_start_time)
        time_label.config(text=f"Time Elapsed: {elapsed_time}s")
        hint_label.config(text=f"Hints Remaining: {hints_remaining}")
        messagebox.showinfo("Game Loaded", "Game loaded successfully.")
    else:
        messagebox.showinfo("No Saved Game", "No saved game found.")

def show_instructions():
    instructions = """
    Hangman Game Instructions:

    1. A random word from a selected category is chosen, and you must guess the letters in the word.
    2. Enter a letter and click 'Submit' to guess.
    3. You have a limited number of incorrect guesses allowed before the hangman is fully drawn.
    4. The game ends when you correctly guess the word or run out of guesses.
    5. Use hints wisely, as you have limited hints available.
    """
    messagebox.showinfo("How to Play", instructions)

def save_high_score(time_taken):
    global high_scores
    name = simpledialog.askstring("High Score!", "You won! Enter your name:")
    if name:
        score_entry = {"name": name, "time": time_taken}
        high_scores.append(score_entry)
        with open("high_scores.json", "w") as f:
            json.dump(high_scores, f)

def display_high_scores():
    global high_scores
    if os.path.exists("high_scores.json"):
        with open("high_scores.json", "r") as f:
            high_scores = json.load(f)
        high_score_text = "\n".join([f"{score['name']}: {score['time']}s" for score in high_scores])
        messagebox.showinfo("High Scores", f"Top High Scores:\n{high_score_text}")
    else:
        messagebox.showinfo("High Scores", "No high scores yet.")

def use_hint():
    global hints_remaining
    if hints_remaining > 0:
        hint_letter = random.choice([letter for letter in word if letter not in guessed_letters])
        guessed_letters.append(hint_letter)
        hints_remaining -= 1
        hint_label.config(text=f"Hints Remaining: {hints_remaining}")
        update_word_display()
    else:
        messagebox.showwarning("No Hints Left", "You have used all your hints.")

def show_game_over_stats(won):
    if won:
        elapsed_time = int(time.time() - game_start_time)
        messagebox.showinfo("You Won!", f"Congratulations! You guessed the word {word} correctly in {elapsed_time} seconds with {correct_guesses} correct guesses and {incorrect_guesses} incorrect guesses.")
        save_high_score(elapsed_time)
    else:
        messagebox.showinfo("Game Over", f"You lost! The word was {word}.")
    reset_game(False)

update_time()
root.mainloop()
