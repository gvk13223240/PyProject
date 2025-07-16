import streamlit as st
from PIL import Image
import io
import os
import time

# Resize image by percentage
def resize_image(image, resize_percent):
    new_width = int(image.width * resize_percent / 100)
    new_height = int(image.height * resize_percent / 100)
    return image.resize((new_width, new_height))

# Compress and return BytesIO
def compress_image(image, quality):
    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=quality)
    buf.seek(0)
    return buf

# Page setup
st.set_page_config(page_title="🗜️ Image Compressor", page_icon="🖼️")
st.title("🗜️ Simple Image Compressor")
st.markdown("Created by **gvk13223240**")

# File uploader
uploaded_file = st.file_uploader(
    "📤 Upload an image",
    type=["jpg", "jpeg", "png", "bmp", "tiff", "tif", "webp", "gif"]
)

if uploaded_file:
    # Open image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="📷 Original Image", use_container_width=True)

    # Show original size in MB
    original_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
    st.write(f"📦 **Original Size:** {original_size_mb:.2f} MB")

    # Compression level selector
    st.subheader("🔧 Select Compression Level")
    compression_choice = st.selectbox(
        "Choose level:",
        ["Low", "Medium", "High", "Custom"]
    )

    if compression_choice == "High":
        resize_percent = 30
        quality = 50
        quality_label = "Low"
    elif compression_choice == "Medium":
        resize_percent = 50
        quality = 70
        quality_label = "Medium"
    elif compression_choice == "Low":
        resize_percent = 70
        quality = 90
        quality_label = "High"
    elif compression_choice == "Custom":
        st.markdown("🎛️ Customize your compression settings:")
        resize_percent = st.slider("Resize %", 10, 100, 50)
        quality = st.slider("JPEG Quality", 10, 100, 70)
        quality_label = f"{quality}%"

    # Compression spinner
    with st.spinner("🔄 Compressing image..."):
        time.sleep(1.5)
        resized_image = resize_image(image, resize_percent)
        compressed_buf = compress_image(resized_image, quality)
        compressed_size_mb = len(compressed_buf.getvalue()) / (1024 * 1024)

    # Display compressed result
    st.success("✅ Compression complete!")
    st.write(f"🗜️ **Compressed Size:** {compressed_size_mb:.2f} MB")
    st.image(compressed_buf, caption=f"Compressed Image ({quality_label} Quality)", use_container_width=True)

    # Download button
    filename = os.path.splitext(uploaded_file.name)[0]
    st.download_button(
        label="⬇️ Download Compressed Image",
        data=compressed_buf,
        file_name=f"{filename}_compressed.jpg",
        mime="image/jpeg"
    )
else:
    st.info("Please upload an image to begin compression.")
