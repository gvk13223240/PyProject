import streamlit as st
from rembg import remove
from PIL import Image
import numpy as np
import io
import cv2

st.set_page_config(page_title="Background Remover & Replacer", layout="centered")

st.title("🪄 Background Remover + Background Replacer")

st.markdown("Upload an image to remove its background and optionally replace it.")

# Upload image
uploaded_image = st.file_uploader("📸 Upload image with background", type=["png", "jpg", "jpeg"])
bg_image = st.file_uploader("🖼️ Upload a new background image (optional)", type=["png", "jpg", "jpeg"])

if uploaded_image:
    # Load uploaded image and remove background
    input_image = Image.open(uploaded_image).convert("RGBA")
    with st.spinner("Removing background..."):
       removed_bg = remove(input_image).convert("RGBA")


    st.markdown("### 🧼 Image after background removal:")
    st.image(removed_bg, use_column_width=True)

    if bg_image:
        bg = Image.open(bg_image).convert("RGBA").resize(removed_bg.size)

        # Composite new background with removed subject
        final_image = Image.alpha_composite(bg, removed_bg)
        st.markdown("### 🎨 Combined Image with New Background:")
        st.image(final_image, use_column_width=True)

        # Download
        buffer = io.BytesIO()
        final_image.save(buffer, format="PNG")
        st.download_button(
            "📥 Download Final Image",
            data=buffer.getvalue(),
            file_name="background_replaced.png",
            mime="image/png"
        )
    else:
        buffer = io.BytesIO()
        removed_bg.save(buffer, format="PNG")
        st.download_button(
            "📥 Download Transparent Image",
            data=buffer.getvalue(),
            file_name="no_background.png",
            mime="image/png"
        )
