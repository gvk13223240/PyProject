import streamlit as st
import numpy as np
from PIL import Image, ImageChops, ImageDraw
from io import BytesIO

st.set_page_config(page_title="Image Difference Highlighter", layout="wide")

st.markdown("<h1 style='text-align: center;'>🖼️ Image Difference Highlighter</h1>", unsafe_allow_html=True)
st.write("Created by - gvk13223240")

resize_option = st.radio("Resize images to match:", ("First Image", "Second Image", "Do Not Resize"))

col1, col2 = st.columns(2)
with col1:
    img1 = st.file_uploader("Upload First Image", type=["png", "jpg", "jpeg"], key="1")
with col2:
    img2 = st.file_uploader("Upload Second Image", type=["png", "jpg", "jpeg"], key="2")

if img1 and img2:
    image1 = Image.open(img1).convert("RGB")
    image2 = Image.open(img2).convert("RGB")

    if resize_option == "First Image":
        image2 = image2.resize(image1.size)
    elif resize_option == "Second Image":
        image1 = image1.resize(image2.size)

    col1, col2 = st.columns(2)
    with col1:
        st.image(image1, caption="Image 1", use_container_width=True)
    with col2:
        st.image(image2, caption="Image 2", use_container_width=True)

    st.markdown("---")
    sensitivity = st.slider("Sensitivity (Lower = More Sensitive)", 1, 100, 50)
    diff = ImageChops.difference(image1, image2)
    diff_np = np.array(diff)
    pixel_diff = np.linalg.norm(diff_np, axis=-1)
    mask = pixel_diff > sensitivity

    highlight_image = image2.copy()
    draw = ImageDraw.Draw(highlight_image)

    labeled_pixels = np.where(mask)
    for y, x in zip(*labeled_pixels):
        draw.rectangle([x-10, y-10, x+10, y+10], outline="red", width=3)

    st.image(highlight_image, caption="🔍 Differences Highlighted", use_container_width=True)

    buf = BytesIO()
    highlight_image.save(buf, format="PNG")
    st.download_button("Download Highlighted Image", buf.getvalue(), file_name="highlighted.png")
