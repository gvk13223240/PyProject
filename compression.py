import streamlit as st
from PIL import Image
import io
import os
import time

# Function to resize the image based on selected percentage
def resize_image(image, resize_percent):
    new_width = int(image.width * resize_percent / 100)
    new_height = int(image.height * resize_percent / 100)
    return image.resize((new_width, new_height))

# Function to compress the image and return it as a BytesIO object
def compress_image(image, quality):
    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=quality)
    buf.seek(0)
    return buf

st.set_page_config(page_title="Image Compressor", page_icon="🗜️")
st.title("🗜️ Simple Image Compressor")
st.write("Created by - gvk13223240")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "bmp", "tiff", "tif", "webp", "gif"])

if uploaded_file:
    # Open and convert the uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_container_width=True)

    # Display original image size in MB
    original_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
    st.write(f"Original Image Size: {original_size_mb:.2f} MB")

    # Compression level selection
    st.write("### Select a Compression Level:")
    compression_choice = st.selectbox(
        "Compression Level",
        ["Low", "Medium", "High", "Custom"]
    )

    # Set resize and quality based on selected compression level
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

    # Start the compression animation
    with st.spinner("Compressing the image... Please wait!"):
        # Simulate compression delay
        time.sleep(2)

        # Resize and compress the image
        resized_image = resize_image(image, resize_percent)
        compressed_image = compress_image(resized_image, quality)

        # Get the size of the compressed image in MB
        compressed_size_mb = len(compressed_image.getvalue()) / (1024 * 1024)

        # Display the result
        st.write(f"🔄 Compression completed! The compressed image size is {compressed_size_mb:.2f} MB.")
        st.image(compressed_image, caption=f"Compressed Image ({quality_level} - {compressed_size_mb:.2f} MB)", use_container_width=True)

        # Allow user to download the compressed image
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
