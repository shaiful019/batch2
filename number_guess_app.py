import tkinter as tk
from tkinter import messagebox
from random import randint
import winsound

class NumberGuessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎲 Number Guessing Game 🎲")
        self.root.geometry("500x450")  # Increased window size
        self.root.configure(bg="#f0e6f6")
        self.number = randint(1, 100)
        self.cnt = 0
        self.history = []
        self.create_widgets()
        self.root.bind('<Return>', lambda event: self.check_guess())  # Bind Enter key to guess

    def create_widgets(self):
        title = tk.Label(self.root, text="Guess the Number!", font=("Arial", 26, "bold"), bg="#f0e6f6", fg="#6a1b9a")
        title.pack(pady=18)

        self.info = tk.Label(self.root, text="I'm thinking of a number between 1 and 100.", font=("Arial", 15), bg="#f0e6f6")
        self.info.pack(pady=7)

        self.entry = tk.Entry(self.root, font=("Arial", 18), width=12, justify='center')
        self.entry.pack(pady=14)
        self.entry.focus()

        self.guess_btn = tk.Button(self.root, text="Guess", font=("Arial", 15, "bold"), bg="#8e24aa", fg="white", command=self.check_guess)
        self.guess_btn.pack(pady=7)

        self.result = tk.Label(self.root, text="", font=("Arial", 17), bg="#f0e6f6")
        self.result.pack(pady=14)

        self.history_label = tk.Label(self.root, text="Your guesses: ", font=("Arial", 12), bg="#f0e6f6", fg="#3949ab")
        self.history_label.pack(pady=7)

        reset_btn = tk.Button(self.root, text="Restart Game", font=("Arial", 12), bg="#3949ab", fg="white", command=self.reset_game)
        reset_btn.pack(pady=7)

        quit_btn = tk.Button(self.root, text="Quit", font=("Arial", 12), bg="#d32f2f", fg="white", command=self.root.quit)
        quit_btn.pack(pady=7)

        # Balloon canvas (hidden by default)
        self.balloon_canvas = tk.Canvas(self.root, width=400, height=180, bg="#f0e6f6", highlightthickness=0)
        self.balloon_canvas.pack(pady=0)
        self.balloon_canvas.place(relx=0.5, rely=0.7, anchor='center')
        self.balloon_canvas.lower("all")

    def play_sound(self, correct):
        if correct:
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        else:
            winsound.Beep(400, 200)

    def show_balloons(self):
        import random
        self.balloon_canvas.lift("all")
        self.balloon_canvas.delete('all')
        colors = ["#ff5252", "#ffb300", "#43a047", "#1e88e5", "#ab47bc", "#f06292"]
        balloons = []
        for i in range(8):
            x = random.randint(30, 370)
            y = 180 + random.randint(0, 40)
            color = random.choice(colors)
            balloon = self.balloon_canvas.create_oval(x, y, x+30, y+40, fill=color, outline="#888", width=2)
            string = self.balloon_canvas.create_line(x+15, y+40, x+15, y+60, fill="#888", width=2)
            balloons.append((balloon, string, x, y))
        self.root.update()
        for step in range(40):
            for balloon, string, x, y in balloons:
                self.balloon_canvas.move(balloon, 0, -4)
                self.balloon_canvas.move(string, 0, -4)
            self.root.update()
            self.balloon_canvas.after(30)
        self.balloon_canvas.after(1000, lambda: self.balloon_canvas.lower("all"))

    def check_guess(self):
        guess = self.entry.get()
        if not guess.isdigit():
            self.result.config(text="Please enter a valid number!", fg="#d32f2f")
            self.play_sound(False)
            return
        guess = int(guess)
        if guess < 1 or guess > 100:
            self.result.config(text="Number must be 1-100!", fg="#d32f2f")
            self.play_sound(False)
            return
        self.cnt += 1
        self.history.append(guess)
        self.history_label.config(text=f"Your guesses: {', '.join(map(str, self.history))}")
        if guess == self.number:
            self.result.config(text=f"🎉 Correct! You guessed in {self.cnt} tries!", fg="#388e3c")
            self.play_sound(True)
            self.show_balloons()
            messagebox.showinfo("🎉 Congratulations! 🎉", f"You guessed the number {self.number} in {self.cnt} tries!\nEnjoy the balloons!")
            self.reset_game(auto=True)
        elif guess < self.number:
            self.result.config(text="⬆️ Too low! Try again.", fg="#1976d2")
            self.play_sound(False)
        else:
            self.result.config(text="⬇️ Too high! Try again.", fg="#d32f2f")
            self.play_sound(False)
        self.entry.delete(0, tk.END)

    def reset_game(self, auto=False):
        self.number = randint(1, 100)
        self.cnt = 0
        self.history = []
        self.result.config(text="")
        self.history_label.config(text="Your guesses: ")
        self.entry.delete(0, tk.END)
        if not auto:
            messagebox.showinfo("Game Reset", "A new number has been chosen! Try again.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessApp(root)
    root.mainloop()
