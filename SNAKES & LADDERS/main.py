import random
import tkinter as tk
from tkinter import messagebox

# ==========================================
# EDITABLE SETTINGS (safe for kids to change)
# ==========================================
BOARD_SIZE = 10  # 10x10 board = 100 squares
SNAKES = {
    99: 54,
    90: 48,
    74: 32,
    62: 19,
    46: 25,
}
LADDERS = {
    2: 38,
    7: 14,
    15: 26,
    21: 42,
    28: 84,
    36: 44,
    51: 67,
    71: 91,
    78: 98,
    87: 94,
}
PLAYER_COLORS = ["#ff4d4d", "#4da6ff"]  # Red, Blue
PLAYER_NAMES = ["Player 1", "Player 2"]


class SnakesAndLadders:
    def __init__(self, root):
        self.root = root
        self.root.title("Snakes & Ladders")

        self.square_size = 50
        canvas_size = self.square_size * BOARD_SIZE

        self.canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="white")
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        self.info_frame = tk.Frame(root)
        self.info_frame.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        self.turn_label = tk.Label(
            self.info_frame, text="Turn: Player 1", font=("Arial", 14, "bold")
        )
        self.turn_label.pack(pady=5)

        self.dice_label = tk.Label(self.info_frame, text="Roll: -", font=("Arial", 14))
        self.dice_label.pack(pady=5)

        self.roll_button = tk.Button(
            self.info_frame, text="Roll Dice", font=("Arial", 12), command=self.roll_dice
        )
        self.roll_button.pack(pady=10)

        self.reset_button = tk.Button(
            self.info_frame, text="Reset Game", font=("Arial", 12), command=self.reset_game
        )
        self.reset_button.pack(pady=5)

        self.players = [0, 0]
        self.current_player = 0
        self.player_tokens = []

        self.draw_board()
        self.draw_snakes_and_ladders()
        self.draw_players()

    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = col * self.square_size
                y1 = (BOARD_SIZE - 1 - row) * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size

                fill_color = "#f2f2f2" if (row + col) % 2 == 0 else "#ffffff"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="#999")

                number = self.square_number(row, col)
                self.canvas.create_text(
                    x1 + 10, y2 - 10, text=str(number), font=("Arial", 8), anchor="sw"
                )

    def draw_snakes_and_ladders(self):
        for start, end in SNAKES.items():
            self.draw_line_between_squares(start, end, color="#8b5a2b", width=4)
        for start, end in LADDERS.items():
            self.draw_line_between_squares(start, end, color="#2e8b57", width=4)

    def draw_players(self):
        for i in range(len(PLAYER_NAMES)):
            token = self.canvas.create_oval(0, 0, 0, 0, fill=PLAYER_COLORS[i], outline="")
            self.player_tokens.append(token)
        self.update_player_positions()

    def square_number(self, row, col):
        if row % 2 == 0:
            return row * BOARD_SIZE + col + 1
        return row * BOARD_SIZE + (BOARD_SIZE - col)

    def number_to_position(self, number):
        number = max(1, min(BOARD_SIZE * BOARD_SIZE, number))
        row = (number - 1) // BOARD_SIZE
        if row % 2 == 0:
            col = (number - 1) % BOARD_SIZE
        else:
            col = BOARD_SIZE - 1 - ((number - 1) % BOARD_SIZE)

        x1 = col * self.square_size
        y1 = (BOARD_SIZE - 1 - row) * self.square_size
        return x1 + self.square_size / 2, y1 + self.square_size / 2

    def update_player_positions(self):
        offsets = [(-10, -10), (10, 10)]
        for i, pos in enumerate(self.players):
            x, y = self.number_to_position(pos if pos > 0 else 1)
            dx, dy = offsets[i]
            size = 14
            self.canvas.coords(
                self.player_tokens[i],
                x - size + dx,
                y - size + dy,
                x + size + dx,
                y + size + dy,
            )

    def draw_line_between_squares(self, start, end, color, width=3):
        x1, y1 = self.number_to_position(start)
        x2, y2 = self.number_to_position(end)
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)

    def roll_dice(self):
        roll = random.randint(1, 6)
        self.dice_label.config(text=f"Roll: {roll}")

        current = self.players[self.current_player]
        new_pos = current + roll

        if new_pos > BOARD_SIZE * BOARD_SIZE:
            self.turn_label.config(
                text=f"{PLAYER_NAMES[self.current_player]} needs exact roll!"
            )
            self.switch_turn()
            return

        if new_pos in SNAKES:
            new_pos = SNAKES[new_pos]
        elif new_pos in LADDERS:
            new_pos = LADDERS[new_pos]

        self.players[self.current_player] = new_pos
        self.update_player_positions()

        if new_pos == BOARD_SIZE * BOARD_SIZE:
            messagebox.showinfo(
                "Winner!",
                f"{PLAYER_NAMES[self.current_player]} wins! 🎉",
            )
            self.roll_button.config(state="disabled")
            return

        self.switch_turn()

    def switch_turn(self):
        self.current_player = (self.current_player + 1) % len(PLAYER_NAMES)
        self.turn_label.config(text=f"Turn: {PLAYER_NAMES[self.current_player]}")

    def reset_game(self):
        self.players = [0, 0]
        self.current_player = 0
        self.dice_label.config(text="Roll: -")
        self.turn_label.config(text="Turn: Player 1")
        self.roll_button.config(state="normal")
        self.update_player_positions()


def main():
    root = tk.Tk()
    SnakesAndLadders(root)
    root.mainloop()


if __name__ == "__main__":
    main()
