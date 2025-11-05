import tkinter as tk
import random
import time

class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Colorful Snake Game")
        self.window.resizable(False, False)
        
        # Game constants
        self.width = 600
        self.height = 400
        self.cell_size = 20
        self.speed = 100  # milliseconds
        
        # Create canvas
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height, bg="black")
        self.canvas.pack()
        
        # Initialize game
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.food = self.create_food()
        self.score = 0
        self.game_over = False
        
        # Color variables
        self.snake_colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]
        self.food_color = "#FF5252"
        self.current_color_index = 0
        
        # Bind keys
        self.window.bind("<KeyPress>", self.change_direction)
        
        # Start game
        self.update()
        
        self.window.mainloop()
    
    def create_food(self):
        while True:
            x = random.randint(0, (self.width - self.cell_size) // self.cell_size) * self.cell_size
            y = random.randint(0, (self.height - self.cell_size) // self.cell_size) * self.cell_size
            food_pos = (x, y)
            if food_pos not in self.snake:
                return food_pos
    
    def change_direction(self, event):
        key = event.keysym
        if key == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif key == "Down" and self.direction != "Up":
            self.direction = "Down"
        elif key == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif key == "Right" and self.direction != "Left":
            self.direction = "Right"
    
    def move_snake(self):
        head_x, head_y = self.snake[0]
        
        if self.direction == "Up":
            new_head = (head_x, head_y - self.cell_size)
        elif self.direction == "Down":
            new_head = (head_x, head_y + self.cell_size)
        elif self.direction == "Left":
            new_head = (head_x - self.cell_size, head_y)
        elif self.direction == "Right":
            new_head = (head_x + self.cell_size, head_y)
        
        # Check for collision with walls
        if (new_head[0] < 0 or new_head[0] >= self.width or 
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            return
        
        # Check for collision with self
        if new_head in self.snake:
            self.game_over = True
            return
        
        self.snake.insert(0, new_head)
        
        # Check if food is eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.create_food()
            # Change snake color
            self.current_color_index = (self.current_color_index + 1) % len(self.snake_colors)
        else:
            self.snake.pop()
    
    def draw(self):
        self.canvas.delete("all")
        
        # Draw snake with gradient colors
        for i, (x, y) in enumerate(self.snake):
            # Calculate color based on position in snake
            color_index = (self.current_color_index + i) % len(self.snake_colors)
            color = self.snake_colors[color_index]
            
            self.canvas.create_rectangle(
                x, y, x + self.cell_size, y + self.cell_size,
                fill=color, outline="", width=0
            )
        
        # Draw food
        self.canvas.create_oval(
            self.food[0], self.food[1],
            self.food[0] + self.cell_size, self.food[1] + self.cell_size,
            fill=self.food_color, outline=""
        )
        
        # Draw score
        self.canvas.create_text(
            50, 20, text=f"Score: {self.score}",
            fill="white", font=("Arial", 14)
        )
        
        # Draw game over message
        if self.game_over:
            self.canvas.create_text(
                self.width // 2, self.height // 2,
                text="GAME OVER", fill="red",
                font=("Arial", 30, "bold")
            )
            self.canvas.create_text(
                self.width // 2, self.height // 2 + 40,
                text=f"Final Score: {self.score}",
                fill="white", font=("Arial", 16)
            )
            self.canvas.create_text(
                self.width // 2, self.height // 2 + 70,
                text="Press 'R' to Restart",
                fill="yellow", font=("Arial", 14)
            )
    
    def update(self):
        if not self.game_over:
            self.move_snake()
            self.draw()
            self.window.after(self.speed, self.update)
        else:
            self.draw()
            self.window.bind("<KeyPress-r>", self.restart_game)
    
    def restart_game(self, event):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.food = self.create_food()
        self.score = 0
        self.game_over = False
        self.current_color_index = 0
        self.window.unbind("<KeyPress-r>")
        self.update()

if __name__ == "__main__":
    SnakeGame()