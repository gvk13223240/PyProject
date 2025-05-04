import streamlit as st
from PIL import Image
import numpy as np
import io

st.set_page_config(page_title="Simple Image Compressor", page_icon="🗜️")
st.title("🗜️ Simple Image Compressor")
st.write("by gvk13223240")

# Upload the image
uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Load and convert image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_container_width=True)

    # Choosing the compression level
    st.write("### 🔧 Select Compression Preset")
    compression_level = st.selectbox(
        "Choose Compression Level",
        ["Low", "Medium", "High"]
    )

    # Set compression parameters
    if compression_level == "Low":
        resize_percent = 30
        quality = 50
    elif compression_level == "Medium":
        resize_percent = 50
        quality = 70
    elif compression_level == "High":
        resize_percent = 70
        quality = 90

    # Resize the image using NumPy + PIL
    image_array = np.array(image)
    new_width = int(image.width * resize_percent / 100)
    new_height = int(image.height * resize_percent / 100)

    resized_image_array = np.array(
        Image.fromarray(image_array).resize((new_width, new_height))
    )
    resized_image = Image.fromarray(resized_image_array)

    # Display compressed image
    st.image(resized_image, caption=f"Compressed Image ({compression_level} Quality)", use_container_width=True)

    # Save and download compressed image
    buf = io.BytesIO()
    resized_image.save(buf, format="JPEG", quality=quality)
    buf.seek(0)

    st.download_button(
        label="⬇️ Download Compressed Image",
        data=buf,
        file_name="compressed_image.jpg",
        mime="image/jpeg"
    )
else:
    st.info("Please upload a JPG or PNG image to compress.")
