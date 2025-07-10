import tkinter as tk
import random
import winsound  # For playing win sound on Windows

# --- Setup main window ---
root = tk.Tk()
root.title("Rock Paper Scissors - AI Mode")
root.geometry("500x400")
root.resizable(False, False)
root.configure(bg="#f0f8ff")

options = ("rock", "paper", "scissors")
player_stats = {}  # Stores each player's history

# --- Player name input ---
name_frame = tk.Frame(root, bg="#f0f8ff")
name_frame.pack(pady=10)

name_label = tk.Label(name_frame, text="Enter your name:", font=("Arial", 10), bg="#f0f8ff")
name_label.pack(side="left")

player_name_var = tk.StringVar()
name_entry = tk.Entry(name_frame, textvariable=player_name_var)
name_entry.pack(side="left")

# --- Labels for result display ---
result_label = tk.Label(root, text="Make your move!", font=("Arial", 16, "bold"), bg="#f0f8ff", fg="#333")
result_label.pack(pady=10)

choice_label = tk.Label(root, text="", font=("Arial", 13), bg="#f0f8ff", fg="#555")
choice_label.pack()

history_label = tk.Label(root, text="", font=("Arial", 10), bg="#f0f8ff", fg="#777")
history_label.pack(pady=5)

score_label = tk.Label(root, text="Wins: 0 | Losses: 0 | Ties: 0", font=("Arial", 11), bg="#f0f8ff", fg="#00688B")
score_label.pack(pady=5)

# --- Flash Animation on Win ---
def animate_win():
    original_color = result_label.cget("fg")
    def flash(count=0):
        if count < 6:
            new_color = "#32CD32" if count % 2 == 0 else original_color
            result_label.config(fg=new_color)
            root.after(150, flash, count + 1)
        else:
            result_label.config(fg=original_color)
    flash()

# --- AI Choice Function ---
def get_ai_choice(name):
    if name not in player_stats:
        return random.choice(options)
    history = player_stats[name]
    total = history["rock"] + history["paper"] + history["scissors"]
    if total == 0:
        return random.choice(options)
    predicted_move = max(["rock", "paper", "scissors"], key=lambda move: history[move])
    return {"rock": "paper", "paper": "scissors", "scissors": "rock"}[predicted_move]

# --- Confetti Canvas Setup ---
confetti_canvas = tk.Canvas(root, width=500, height=400, bg="#f0f8ff", highlightthickness=0)
confetti_canvas.place(x=0, y=0, width=500, height=400)
confetti_canvas.tk.call("lower", confetti_canvas._w)  # start behind other widgets


# --- Sparkle Animation ---
sparkle_particles = []
def start_sparkles():
    sparkle_particles.clear()
    for _ in range(50):
        x = random.randint(0, 500)
        y = random.randint(0, 400)
        size = random.randint(2, 4)
        color = random.choice(["#FFFFE0", "#FFFFFF", "#FFFACD"])
        particle = confetti_canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
        sparkle_particles.append(particle)
    def sparkle_animation(step=0):
        if step < 50:
            for particle in sparkle_particles:
                current_color = confetti_canvas.itemcget(particle, "fill")
                new_color = "" if current_color else random.choice(["#FFFFE0", "#FFFFFF", "#FFFACD"])
                confetti_canvas.itemconfig(particle, fill=new_color)
            root.after(100, sparkle_animation, step + 1)
        else:
            for particle in sparkle_particles:
                confetti_canvas.delete(particle)
            sparkle_particles.clear()
    sparkle_animation()

# --- Confetti Animation ---
def start_confetti():
    particles = []
    for _ in range(100):
        x = random.randint(0, 500)
        y = random.randint(-200, 0)
        size = random.randint(5, 10)
        color = random.choice(["#FF69B4", "#FFD700", "#00FA9A", "#1E90FF", "#FF4500"])
        shape = confetti_canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
        particles.append((shape, random.uniform(1, 4)))

    confetti_canvas.lift()  # bring confetti canvas above all widgets
    start_sparkles()

    def animate(step=0):
        if step < 50:
            for shape, speed in particles:
                confetti_canvas.move(shape, 0, speed)
            root.after(50, animate, step + 1)
        else:
            for shape, _ in particles:
                confetti_canvas.delete(shape)
            confetti_canvas.lower()  # send canvas behind widgets after animation ends

    animate()

# --- Game Play ---
def play(player_choice):
    name = player_name_var.get().strip() or "Player"
    if name not in player_stats:
        player_stats[name] = {"rock": 0, "paper": 0, "scissors": 0, "wins": 0, "losses": 0, "ties": 0}
    player_stats[name][player_choice] += 1
    computer_choice = get_ai_choice(name)
    if player_choice == computer_choice:
        player_stats[name]["ties"] += 1
        result = "It's a tie!"
    elif (player_choice == "rock" and computer_choice == "scissors") or \
         (player_choice == "paper" and computer_choice == "rock") or \
         (player_choice == "scissors" and computer_choice == "paper"):
        player_stats[name]["wins"] += 1
        result = f"{name} wins!"
    else:
        player_stats[name]["losses"] += 1
        result = f"{name} loses!"

    # Update result and score before any animation or sound
    result_label.config(text=result)
    score_label.config(text=f"Wins: {player_stats[name]['wins']} | Losses: {player_stats[name]['losses']} | Ties: {player_stats[name]['ties']}")
    root.update_idletasks()

    # Continue with effects if win
    if result.endswith("wins!"):
        winsound.PlaySound("win.wav", winsound.SND_FILENAME)
        animate_win()
        start_confetti()

    choice_label.config(text=f"{name} chose: {player_choice} | Computer: {computer_choice}")
    history_label.config(text=f"History: {player_stats[name]}")

# --- Reset Stats ---
def reset_history():
    name = player_name_var.get().strip() or "Player"
    player_stats[name] = {"rock": 0, "paper": 0, "scissors": 0, "wins": 0, "losses": 0, "ties": 0}
    history_label.config(text="History: Reset")
    result_label.config(text="Make your move!")
    choice_label.config(text="")
    score_label.config(text="Wins: 0 | Losses: 0 | Ties: 0")

# --- Show All Players Detailed History ---
def show_player_history():
    if not player_stats:
        msg = "No player data available."
    else:
        msg = "\U0001F4CA All Player Histories:\n\n"
        for name, stats in player_stats.items():
            msg += (
                f"{name} - Rock: {stats['rock']}, Paper: {stats['paper']}, Scissors: {stats['scissors']}, "
                f"Wins: {stats['wins']}, Losses: {stats['losses']}, Ties: {stats['ties']}\n"
            )

    popup = tk.Toplevel(root)
    popup.title("All Player Histories")
    popup.geometry("360x300")
    popup.configure(bg="#fffaf0")
    tk.Label(popup, text=msg, font=("Arial", 10), justify="left", bg="#fffaf0", fg="#333").pack(padx=10, pady=10)
    tk.Button(popup, text="Close", command=popup.destroy, bg="#f08080", width=15).pack(pady=10)

# --- Show Leaderboard ---
def show_all_histories():
    if not player_stats:
        msg = "No players have played yet."
    else:
        sorted_stats = sorted(player_stats.items(), key=lambda x: x[1]['wins'], reverse=True)
        msg = "\U0001F465 Leaderboard (Sorted by Wins):\n\n"
        for name, stats in sorted_stats:
            msg += f"{name} - Wins: {stats['wins']}, Losses: {stats['losses']}, Ties: {stats['ties']}\n"

    popup = tk.Toplevel(root)
    popup.title("Leaderboard")
    popup.geometry("340x300")
    popup.configure(bg="#f5fffa")
    tk.Label(popup, text=msg, font=("Arial", 10), justify="left", bg="#f5fffa", fg="#222").pack(padx=10, pady=10)
    tk.Button(popup, text="Close", command=popup.destroy, bg="#f08080", width=15).pack(pady=10)

# --- Buttons ---
button_frame = tk.Frame(root, bg="#f0f8ff")
button_frame.pack(pady=15)
style_btn = {"width": 12, "font": ("Arial", 11, "bold"), "bg": "#add8e6", "fg": "#000", "activebackground": "#87ceeb"}

tk.Button(button_frame, text="Rock", command=lambda: play("rock"), **style_btn).grid(row=0, column=0, padx=8)
tk.Button(button_frame, text="Paper", command=lambda: play("paper"), **style_btn).grid(row=0, column=1, padx=8)
tk.Button(button_frame, text="Scissors", command=lambda: play("scissors"), **style_btn).grid(row=0, column=2, padx=8)

tk.Button(root, text="Reset Game", width=20, font=("Arial", 10), command=reset_history, bg="#dcdcdc").pack(pady=5)
tk.Button(root, text="Show All History", width=20, font=("Arial", 10), command=show_player_history, bg="#ffe4b5").pack(pady=5)
tk.Button(root, text="Show Leaderboard", width=20, font=("Arial", 10), command=show_all_histories, bg="#e0ffff").pack(pady=5)
tk.Button(root, text="Exit", width=20, font=("Arial", 10), command=root.quit, bg="#f08080").pack(pady=5)

# --- Start App ---
root.mainloop()
