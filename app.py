import streamlit as st
import random
import os
from dotenv import load_dotenv
from streamlit_oauth import OAuth2Component

# Load environment variables
if "STREAMLIT_SERVER_PORT" not in os.environ:
    load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID") or st.secrets.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET") or st.secrets.get("GOOGLE_CLIENT_SECRET")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID") or st.secrets.get("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET") or st.secrets.get("GITHUB_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI") or st.secrets.get("REDIRECT_URI") or "http://localhost:8501"

# OAuth2 Setup
google = OAuth2Component(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    authorize_endpoint="https://accounts.google.com/o/oauth2/auth",
    token_endpoint="https://oauth2.googleapis.com/token",
    revoke_token_endpoint="https://oauth2.googleapis.com/revoke"
)

github = OAuth2Component(
    client_id=GITHUB_CLIENT_ID,
    client_secret=GITHUB_CLIENT_SECRET,
    authorize_endpoint="https://github.com/login/oauth/authorize",
    token_endpoint="https://github.com/login/oauth/access_token"
)

# Login UI
st.title("🐍 Snake Game")
google_user = google.authorize_button(
    name="Login with Google",
    redirect_uri=REDIRECT_URI,
    scope="openid email profile",
    extras_params={"access_type": "offline", "prompt": "consent"},
    pkce="S256"
)

github_user = github.authorize_button(
    name="Login with GitHub",
    redirect_uri=REDIRECT_URI,
    scope="read:user"
)

if google_user and "user_info" not in st.session_state:
    st.session_state.user_info = google_user
    st.session_state.provider = "google"

if github_user and "user_info" not in st.session_state:
    st.session_state.user_info = github_user
    st.session_state.provider = "github"

user_info = st.session_state.get("user_info")

if not user_info:
    st.warning("🔐 Please log in to play the game.")
    st.stop()

# Game constants
ROWS, COLS = 10, 10
DIRS = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}

# Snake & Node classes
class Node:
    def __init__(self, position):
        self.position = position
        self.next = None

class Snake:
    def __init__(self, start_pos):
        self.head = Node(start_pos)
        self.tail = self.head
        self.positions = {start_pos}

    def move(self, new_pos, grow=False):
        new_head = Node(new_pos)
        new_head.next = self.head
        self.head = new_head
        self.positions.add(new_pos)
        if not grow:
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

# Game state init
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
        return

    head_x, head_y = st.session_state.snake.head.position
    dx, dy = DIRS[st.session_state.direction]
    new_head = (head_x + dx, head_y + dy)

    if not (0 <= new_head[0] < ROWS and 0 <= new_head[1] < COLS) or new_head in st.session_state.snake.positions:
        st.session_state.game_over = True
        return

    grow = new_head == st.session_state.food
    if grow:
        st.session_state.score += 1
        st.session_state.food = place_food(st.session_state.snake.positions)

    st.session_state.snake.move(new_head, grow=grow)

# --- UI Layout ---
st.caption(f"Welcome, {user_info.get('name') or user_info.get('login')}! Click Logout in sidebar to end session.")
if st.sidebar.button("Logout"):
    if st.session_state.provider == "google":
        google.revoke_token(user_info.get("token", {}))
    elif st.session_state.provider == "github":
        github.revoke_token(user_info.get("token", {}))
    st.session_state.clear()
    st.experimental_rerun()

if "snake" not in st.session_state:
    init()

# Direction Controls
st.subheader("🎮 Controller")
top = st.columns(3)
with top[1]:
    if st.button("⬆️") and st.session_state.direction != "Down":
        st.session_state.direction = "Up"

middle = st.columns(3)
with middle[0]:
    if st.button("⬅️") and st.session_state.direction != "Right":
        st.session_state.direction = "Left"
with middle[2]:
    if st.button("➡️") and st.session_state.direction != "Left":
        st.session_state.direction = "Right"

bottom = st.columns(3)
with bottom[1]:
    if st.button("⬇️") and st.session_state.direction != "Up":
        st.session_state.direction = "Down"

# Restart Button
if st.button("🔁 Restart"):
    init()

# Game Logic & Grid
step()
st.markdown(f"**🏆 Score:** {st.session_state.score}")
draw_grid()

# Game Over Message
if st.session_state.game_over:
    st.error("💥 Game Over! Click Restart to play again.")
