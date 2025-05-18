import streamlit as st
import random
import time

# Grid size
ROWS, COLS = 10, 10

# Directions
DIRS = {
    "Up": (-1, 0),
    "Down": (1, 0),
    "Left": (0, -1),
    "Right": (0, 1),
}

# Snake node for linked list
class Node:
    def __init__(self, position):
        self.position = position
        self.next = None

# Snake class implemented as a linked list
class Snake:
    def __init__(self, start_pos):
        self.head = Node(start_pos)
        self.tail = self.head
        self.positions = {start_pos}  # Set for quick lookup

    def move(self, new_pos, grow=False):
        # Add new head node
        new_head = Node(new_pos)
        new_head.next = self.head
        self.head = new_head
        self.positions.add(new_pos)

        if not grow:
            # Remove tail node
            # Find second last node
            current = self.head
            while current.next != self.tail:
                current = current.next
            self.positions.remove(self.tail.position)
            current.next = None
            self.tail = current

    def get_positions(self):
        pos = []
        current = self.head
        while current:
            pos.append(current.position)
            current = current.next
        return pos

# Initialize game state
def init():
    st.session_state.snake = Snake((ROWS//2, COLS//2))
    st.session_state.direction = "Right"
    st.session_state.food = place_food(st.session_state.snake.positions)
    st.session_state.score = 0
    st.session_state.game_over = False

def place_food(snake_positions):
    while True:
        pos = (random.randint(0, ROWS-1), random.randint(0, COLS-1))
        if pos not in snake_positions:
            return pos

def draw_grid():
    grid = []
    snake_positions = set(st.session_state.snake.get_positions())
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            if (i, j) == st.session_state.food:
                row.append("🍎")
            elif (i, j) == st.session_state.snake.head.position:
                row.append("🟩")
            elif (i, j) in snake_positions:
                row.append("🟢")
            else:
                row.append("⬜")
        grid.append("".join(row))
    st.text("\n".join(grid))

def step():
    if st.session_state.game_over:
        st.warning("Game Over! Press Restart to play again.")
        return

    head_x, head_y = st.session_state.snake.head.position
    dx, dy = DIRS[st.session_state.direction]
    new_head = (head_x + dx, head_y + dy)

    # Check collisions with walls
    if not (0 <= new_head[0] < ROWS and 0 <= new_head[1] < COLS):
        st.session_state.game_over = True
        return

    # Check collision with itself
    if new_head in st.session_state.snake.positions:
        st.session_state.game_over = True
        return

    # Check if food eaten
    grow = False
    if new_head == st.session_state.food:
        grow = True
        st.session_state.score += 1
        st.session_state.food = place_food(st.session_state.snake.positions)

    st.session_state.snake.move(new_head, grow=grow)

# --- Streamlit app ---

st.title("🐍 Snake Game with Linked List")

if "snake" not in st.session_state:
    init()

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Up"):
        if st.session_state.direction != "Down":
            st.session_state.direction = "Up"
with col2:
    if st.button("Left"):
        if st.session_state.direction != "Right":
            st.session_state.direction = "Left"
with col3:
    if st.button("Right"):
        if st.session_state.direction != "Left":
            st.session_state.direction = "Right"
with col4:
    if st.button("Down"):
        if st.session_state.direction != "Up":
            st.session_state.direction = "Down"

if st.button("Restart"):
    init()

step()

st.markdown(f"**Score:** {st.session_state.score}")
draw_grid()

if st.session_state.game_over:
    st.error("💥 Game Over! Try again.")
