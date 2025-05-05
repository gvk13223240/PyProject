import streamlit as st
from PIL import Image
import io
import os

def resize_image(image, resize_percent):
    new_width = int(image.width * resize_percent / 100)
    new_height = int(image.height * resize_percent / 100)
    return image.resize((new_width, new_height))

def compress_image(image, quality):
    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=quality)
    buf.seek(0)
    return buf

st.set_page_config(page_title="Image Compressor", page_icon="🗜️")
st.title("🗜️ Simple Image Compressor")
st.write("Created by - gvk13223240")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_container_width=True)

    st.write("### Select a Compression Level:")
    compression_choice = st.selectbox(
        "Compression Level",
        ["Low", "Medium", "High", "Custom"]
    )

    if compression_choice == "High":
        resize_percent = 30
        quality = 50
        quality_level = "Low Quality"
    elif compression_choice == "Medium":
        resize_percent = 50
        quality = 70
        quality_level = "Medium Quality"
    elif compression_choice == "Low":
        resize_percent = 70
        quality = 90
        quality_level = "High Quality"
    elif compression_choice == "Custom":
        st.write("You have selected the **Custom Compression Settings** option.")
        resize_percent = st.slider("Resize Percentage", min_value=10, max_value=100, value=50)
        quality = st.slider("Compression Quality", min_value=10, max_value=100, value=70)
        quality_level = f"{quality}% Quality"

    resized_image = resize_image(image, resize_percent)
    compressed_image = compress_image(resized_image, quality)
    actual_size_kb = len(compressed_image.getvalue()) / 1024

    st.write("🔄 Compressing...")
    st.image(compressed_image, caption=f"Compressed Image ({quality_level} - {actual_size_kb:.2f} KB)", use_container_width=True)

    base_filename = os.path.splitext(uploaded_file.name)[0]
    file_name = f"{base_filename}_compressed.jpg"

    st.download_button(
        label="⬇️ Download Compressed Image",
        data=compressed_image,
        file_name=file_name,
        mime="image/jpeg"
    )
else:
    st.info("Please upload an image to compress.")
