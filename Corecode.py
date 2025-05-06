import streamlit as st
import numpy as np
from PIL import Image, ImageChops, ImageDraw

st.set_page_config(page_title="Image Difference Highlighter", layout="wide")

st.markdown("<h1 style='text-align: center;'>🖼️ Image Difference Highlighter</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    img1 = st.file_uploader("Upload First Image", type=["png", "jpg", "jpeg"], key="1")
with col2:
    img2 = st.file_uploader("Upload Second Image", type=["png", "jpg", "jpeg"], key="2")

if img1 and img2:
    image1 = Image.open(img1).convert("RGB")
    image2 = Image.open(img2).convert("RGB")
    image2 = image2.resize(image1.size)
    diff = ImageChops.difference(image1, image2)
    diff_np = np.array(diff)
    mask = np.any(diff_np > 30, axis=-1)
    highlight = image2.copy()
    draw = ImageDraw.Draw(highlight)
    ys, xs = np.where(mask)
    for x, y in zip(xs, ys):
        draw.point((x, y), fill=(255, 0, 0))
    col1, col2 = st.columns(2)
    with col1:
        st.image(image1, caption="Image 1", use_container_width=True)
    with col2:
        st.image(image2, caption="Image 2 (Resized)", use_container_width=True)
    st.markdown("---")
    st.image(highlight, caption="🔍 Differences Highlighted", use_container_width=True)
