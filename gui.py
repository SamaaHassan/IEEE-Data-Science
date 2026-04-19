

import tkinter as tk
from tkinter import messagebox
import game_logic as logic  # Import game logic
from config import GAME_CONFIG # Import configuration settings

# Modern UI Palette
COLORS = {
    "primary": "#2D1B36",    # Midnight Purple (Background)
    "secondary": "#4B3061",  # Light Purple (Cards)
    "accent": "#F9E4B7",     # Creamy Gold (Buttons and key text)
    "white": "#FFFFFF",      # White for text
    "success": "#4CAF50",    # Green for win
    "fail": "#F44336",       # Red for loss
    "hover": "#63447D"       # Hover color for buttons
}

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Star Guess Pro 🚀")
        self.root.geometry("400x700")
        self.root.configure(bg=COLORS["primary"])
        self.root.resizable(False, False)

        # Game State Variables
        self.current_level_data = None
        self.secret_number = 0
        self.attempts_left = 0
        self.game_active = True # Control game state and button activity

        # Main Screen Container
        self.main_container = tk.Frame(self.root, bg=COLORS["primary"])
        self.main_container.pack(fill="both", expand=True)

        self.show_welcome_screen()

    def clear_container(self):
        """Clears current screen content before navigating to the next"""
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # --- 1. Welcome Screen ---
    def show_welcome_screen(self):
        self.clear_container()
        frame = tk.Frame(self.main_container, bg=COLORS["primary"])
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="⭐ ⭐ ⭐", fg=COLORS["accent"], bg=COLORS["primary"], font=("Arial", 20)).pack()
        tk.Label(frame, text="Welcome to the\nNumber Guessing Game!", 
                 fg=COLORS["white"], bg=COLORS["primary"], 
                 font=("Comic Sans MS", 20, "bold"), justify="center").pack(pady=20)
        
        tk.Label(frame, text="Loading Universe...", fg=COLORS["accent"], bg=COLORS["primary"], font=("Arial", 10, "italic")).pack()

        # Smooth transition after 2 seconds
        self.root.after(2000, self.show_levels_menu)

    # --- 2. Levels Menu ---
    def show_levels_menu(self):
        self.clear_container()
        
        tk.Label(self.main_container, text="Select Difficulty", fg=COLORS["accent"], 
                 bg=COLORS["primary"], font=("Arial", 24, "bold")).pack(pady=(50, 30))

        # Dynamically load levels from Config
        for key, level in GAME_CONFIG.items():
            level_frame = tk.Frame(self.main_container, bg=COLORS["secondary"], pady=10, padx=10)
            level_frame.pack(pady=10, padx=40, fill="x")

            info_text = f"Level {key}: {level['name']}\nGuess 1-{level['limit']} | {level['max_trials']} Tries"
            
            btn = tk.Button(level_frame, text=info_text, 
                            command=lambda l=level: self.start_game(l),
                            bg=COLORS["secondary"], fg=COLORS["white"], 
                            font=("Arial", 11, "bold"), bd=0, cursor="hand2",
                            activebackground=COLORS["accent"], activeforeground=COLORS["primary"])
            btn.pack(fill="x")

            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=COLORS["hover"]))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=COLORS["secondary"]))

    # --- 3. Game Screen ---
    def start_game(self, level_data):
        self.current_level_data = level_data
        self.secret_number = logic.generate_secret_number(level_data['limit'])
        self.attempts_left = level_data['max_trials']
        self.game_active = True
        
        self.clear_container()
        
        # Attempts Information
        stats_frame = tk.Frame(self.main_container, bg=COLORS["primary"])
        stats_frame.pack(fill="x", pady=20, padx=20)
        
        self.attempts_label = tk.Label(stats_frame, text=f"Attempts Left: {self.attempts_left}", 
                                      fg=COLORS["accent"], bg=COLORS["primary"], font=("Arial", 12, "bold"))
        self.attempts_label.pack(side="left")

        # Instructions
        tk.Label(self.main_container, text=f"Guess between 1 and {level_data['limit']}", 
                 fg=COLORS["white"], bg=COLORS["primary"], font=("Arial", 14)).pack(pady=10)

        # Mystery Box
        self.box_frame = tk.Frame(self.main_container, bg=COLORS["accent"], width=160, height=160)
        self.box_frame.pack_propagate(False)
        self.box_frame.pack(pady=20)
        
        self.display_num = tk.Label(self.box_frame, text="?", fg=COLORS["primary"], 
                                   bg=COLORS["accent"], font=("Arial", 70, "bold"))
        self.display_num.pack(expand=True)

        # Feedback & Messages
        self.feedback_label = tk.Label(self.main_container, text="Ready? Enter a number!", 
                                      fg=COLORS["white"], bg=COLORS["primary"], font=("Arial", 14, "bold"))
        self.feedback_label.pack(pady=10)

        # Input & Guess Button
        self.input_frame = tk.Frame(self.main_container, bg=COLORS["accent"], padx=5, pady=5)
        self.input_frame.pack(pady=10)

        self.entry = tk.Entry(self.input_frame, width=5, font=("Arial", 28), bd=0, justify="center")
        self.entry.pack(side="left")
        self.entry.focus_set()

        self.guess_btn = tk.Button(self.input_frame, text="GUESS", command=self.check_guess, 
                                  bg=COLORS["accent"], fg=COLORS["primary"], 
                                  font=("Arial", 14, "bold"), bd=0, cursor="hand2")
        self.guess_btn.pack(side="left", padx=10)

        # Visual Progress Bar
        self.progress_canvas = tk.Canvas(self.main_container, width=200, height=10, 
                                        bg=COLORS["secondary"], highlightthickness=0)
        self.progress_canvas.pack(pady=20)
        self.update_progress_bar()

        # Navigation Controls
        nav_frame = tk.Frame(self.main_container, bg=COLORS["primary"])
        nav_frame.pack(side="bottom", pady=30)

        self.cont_btn = tk.Button(nav_frame, text="↺ Continue Playing", command=lambda: self.start_game(self.current_level_data),
                  bg=COLORS["primary"], fg=COLORS["accent"], bd=0, font=("Arial", 11, "underline"), cursor="hand2")
        self.cont_btn.pack(side="left", padx=15)
        
        self.menu_btn = tk.Button(nav_frame, text="🏠 Back to Menu", command=self.show_levels_menu, 
                  bg=COLORS["primary"], fg=COLORS["accent"], bd=0, font=("Arial", 11, "underline"), cursor="hand2")
        self.menu_btn.pack(side="left", padx=15)

    def check_guess(self):
        if not self.game_active: return # Disable input if game is over

        val = self.entry.get()
        if not logic.validate_input(val):
            self.feedback_label.config(text="⚠️ Enter a Number!", fg=COLORS["fail"])
            return

        guess = int(val)
        result = logic.process_guess(guess, self.secret_number)
        self.attempts_left -= 1
        self.update_progress_bar()
        self.attempts_label.config(text=f"Attempts Left: {self.attempts_left}")

        if result == "win":
            self.end_round(True)
        elif self.attempts_left <= 0:
            self.end_round(False)
        else:
            hint = "Higher ⬆️" if result == "increase" else "Lower ⬇️"
            self.feedback_label.config(text=f"No, try {hint}!", fg=COLORS["accent"])
        
        self.entry.delete(0, tk.END)

    def update_progress_bar(self):
        """Updates the visual progress bar based on attempts left"""
        self.progress_canvas.delete("all")
        max_t = self.current_level_data['max_trials']
        width = (self.attempts_left / max_t) * 200
        self.progress_canvas.create_rectangle(0, 0, width, 10, fill=COLORS["accent"], outline="")

    def end_round(self, won):
        """Displays final result and disables inputs"""
        self.game_active = False
        self.display_num.config(text=str(self.secret_number)) # Reveal number
        
        # Disable input field and guess button visually and functionally
        self.guess_btn.config(state="disabled", bg="#888888")
        self.entry.config(state="disabled")

        if won:
            self.feedback_label.config(text="🎉 YOU WON! 🎉", fg=COLORS["success"])
        else:
            self.feedback_label.config(text=f"💥 GAME OVER! IT WAS {self.secret_number}", fg=COLORS["fail"])
        
        # Highlight next action buttons
        self.cont_btn.config(font=("Arial", 12, "bold", "underline"))
        self.menu_btn.config(font=("Arial", 12, "bold", "underline"))

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()