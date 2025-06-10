import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import os
import json

# Optional: use if you want the image comparison feature
# pip install streamlit-image-comparison
from streamlit_image_comparison import image_comparison


# ---------------------------
# USER AUTH
# ---------------------------
USERS = {
    "alice": "pass123",
    "bob": "hello456"
}

def login():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if USERS.get(username) == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Invalid credentials")

def logout():
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.rerun()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""

if not st.session_state.authenticated:
    login()
    st.stop()
else:
    st.sidebar.write(f"👤 Logged in as: `{st.session_state.username}`")
    if st.sidebar.button("Logout"):
        logout()

# ---------------------------
# FILTER FUNCTIONS
# ---------------------------
def apply_overlay(image, color_bgr, strength):
    overlay = np.full_like(image, color_bgr, dtype=np.uint8)
    return cv2.addWeighted(image, 1 - strength, overlay, strength, 0)

def apply_grayscale(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

def apply_invert(image):
    return cv2.bitwise_not(image)

def apply_blur(image):
    return cv2.GaussianBlur(image, (15, 15), 0)

def apply_edge(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edge = cv2.Canny(gray, 100, 200)
    return cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

def apply_vignette(image):
    rows, cols = image.shape[:2]
    kernel_x = cv2.getGaussianKernel(cols, cols / 2)
    kernel_y = cv2.getGaussianKernel(rows, rows / 2)
    kernel = kernel_y * kernel_x.T
    mask = kernel / kernel.max()
    vignette = np.copy(image)
    for i in range(3):
        vignette[:, :, i] = vignette[:, :, i] * mask
    return vignette

def apply_cartoon(image):
    # Enhanced OpenCV-based cartoon effect
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY, 9, 9
    )
    color = cv2.bilateralFilter(image, d=9, sigmaColor=200, sigmaSpace=200)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

def apply_beautify(image):
    return cv2.bilateralFilter(image, 15, 75, 75)

# ---------------------------
# PRESET STORAGE
# ---------------------------
PRESET_DIR = "presets"
os.makedirs(PRESET_DIR, exist_ok=True)

def get_preset_path(username):
    return os.path.join(PRESET_DIR, f"{username}_presets.json")

def save_preset(username, filters):
    path = get_preset_path(username)
    with open(path, "w") as f:
        json.dump(filters, f)

def load_preset(username):
    path = get_preset_path(username)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

# ---------------------------
# UI
# ---------------------------
st.title("🎨 Image Filter App")
st.caption("Apply filters, save presets, and preview changes interactively.")

uploaded_img = st.file_uploader("📁 Upload a base image", type=["png", "jpg", "jpeg"])
uploaded_filter = st.file_uploader("🎨 Upload a filter overlay image (optional)", type=["png", "jpg", "jpeg"])
strength = st.slider("🌀 Custom Filter Strength (if used)", 0.0, 1.0, 0.4, 0.05)

st.markdown("### 🧰 Choose Filters")
col1, col2, col3 = st.columns(3)
with col1:
    warm = st.checkbox("Warm")
    cool = st.checkbox("Cool")
    sepia = st.checkbox("Sepia")
with col2:
    grayscale = st.checkbox("Grayscale")
    invert = st.checkbox("Invert")
    beautify = st.checkbox("Beautify")
with col3:
    blur = st.checkbox("Blur")
    edge = st.checkbox("Edge")
    vignette = st.checkbox("Vignette")
    cartoon = st.checkbox("Cartoon")

if st.button("💾 Save Preset"):
    filters = {
        "warm": warm, "cool": cool, "sepia": sepia,
        "grayscale": grayscale, "invert": invert,
        "blur": blur, "edge": edge, "vignette": vignette,
        "cartoon": cartoon, "beautify": beautify
    }
    save_preset(st.session_state.username, filters)
    st.success("Preset saved!")

if st.button("📥 Load Preset"):
    preset = load_preset(st.session_state.username)
    if preset:
        warm = preset.get("warm", False)
        cool = preset.get("cool", False)
        sepia = preset.get("sepia", False)
        grayscale = preset.get("grayscale", False)
        invert = preset.get("invert", False)
        blur = preset.get("blur", False)
        edge = preset.get("edge", False)
        vignette = preset.get("vignette", False)
        cartoon = preset.get("cartoon", False)
        beautify = preset.get("beautify", False)
        st.success("Preset loaded! Reloading page...")
        st.rerun()
    else:
        st.warning("No preset found.")

if uploaded_img:
    original_pil = Image.open(uploaded_img).convert("RGB")
    img = cv2.cvtColor(np.array(original_pil), cv2.COLOR_RGB2BGR)

    if uploaded_filter:
        filter_pil = Image.open(uploaded_filter).convert("RGB")
        filter_cv = cv2.cvtColor(np.array(filter_pil), cv2.COLOR_RGB2BGR)
        filter_resized = cv2.resize(filter_cv, (img.shape[1], img.shape[0]))
        img = cv2.addWeighted(img, 1 - strength, filter_resized, strength, 0)

    if warm:
        img = apply_overlay(img, (20, 100, 200), 0.4)
    if cool:
        img = apply_overlay(img, (200, 100, 20), 0.4)
    if sepia:
        img = apply_overlay(img, (50, 100, 150), 0.4)
    if grayscale:
        img = apply_grayscale(img)
    if invert:
        img = apply_invert(img)
    if beautify:
        img = apply_beautify(img)
    if blur:
        img = apply_blur(img)
    if edge:
        img = apply_edge(img)
    if vignette:
        img = apply_vignette(img)
    if cartoon:
        img = apply_cartoon(img)

    result_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    # Add small watermark to corner
    watermark_text = "© VKG"
    draw = ImageDraw.Draw(result_pil)
    font_size = 10
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    text_position = (result_pil.width - 50, result_pil.height - 20)
    draw.text(text_position, watermark_text, fill=(180, 180, 180), font=font)

    st.markdown("### 🎚️ Compare Before and After")
    image_comparison(
        img1=original_pil,
        img2=result_pil,
        label1="Original",
        label2="Filtered"
    )

    st.markdown("### 📥 Download Result")
    buffer = io.BytesIO()
    result_pil.save(buffer, format="PNG")
    st.download_button("Download Filtered Image", data=buffer.getvalue(), file_name="filtered_output.png")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 12px;'>Made by Vamshi Krishna G.......</div>",
    unsafe_allow_html=True
)
