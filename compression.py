# import streamlit as st
# from PIL import Image
# import numpy as np
# import io

# st.set_page_config(page_title="Simple Image Compressor", page_icon="🗜️")
# st.title("🗜️ Simple Image Compressor")
# st.write("by gvk13223240")

# uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

# if uploaded_file:
#     image = Image.open(uploaded_file).convert("RGB")
#     st.image(image, caption="Original Image", use_container_width=True)

#     st.write("### 🔧 Select Compression Preset")
#     compression_level = st.selectbox(
#         "Choose Compression Level",
#         ["Low", "Medium", "High"]
#     )

#     if compression_level == "High":
#         resize_percent = 30
#         quality = 50
#         quality_level="Low"
#     elif compression_level == "Medium":
#         resize_percent = 50
#         quality = 70
#         quality_level="Medium"
#     elif compression_level == "Low":
#         resize_percent = 70
#         quality = 90
#         quality_level="High"

#     new_width = int(image.width * resize_percent / 100)
#     new_height = int(image.height * resize_percent / 100)
#     resized_image = image.resize((new_width, new_height))

#     buf = io.BytesIO()
#     resized_image.save(buf, format="JPEG", quality=quality)
#     buf.seek(0)
#     compressed_size_kb = len(buf.getvalue()) / 1024

#     st.image(resized_image, caption=f"Compressed Image ({quality_level} Quality - {compressed_size_kb:.2f} KB)", use_container_width=True)

#     st.download_button(
#         label="⬇️ Download Compressed Image",
#         data=buf,
#         file_name="compressed_image.jpg",
#         mime="image/jpeg"
#     )
# else:
#     st.info("Please upload a JPG or PNG image to compress.")
import streamlit as st
from PIL import Image
import io

def resize_image(image, resize_percent):
    new_width = int(image.width * resize_percent / 100)
    new_height = int(image.height * resize_percent / 100)
    return image.resize((new_width, new_height))

def compress_image(image, quality):
    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=quality)
    buf.seek(0)
    return buf

# Set page config and title
st.set_page_config(page_title="Image Compressor", page_icon="🗜️")
st.title("🗜️ Simple Image Compressor")

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_container_width=True)

    # Radio button for preset compression level
    st.write("### Choose Compression Level (Preset Options)")
    compression_level = st.selectbox(
        "Choose Compression Level",
        ["Low", "Medium", "High"]
    )

    # Default values based on preset compression level
    if compression_level == "High":
        resize_percent = 30
        quality = 50
        qualit_level="Low"
    elif compression_level == "Medium":
        resize_percent = 50
        quality = 70
        qualit_level="Medium"
    elif compression_level == "Low":
        resize_percent = 70
        quality = 90
        qualit_level="High"
    st.write(f"Compression Level: {compression_level} ({resize_percent}% size, {quality}% quality)")

    # Option for advanced settings (custom user input)
    st.write("### Advanced Compression Settings (Optional)")
    advanced_settings = st.checkbox("Use Custom Compression Settings")

    if advanced_settings:
        st.write("You can adjust the compression and resize settings manually:")
        resize_percent = st.slider("Resize Percentage", min_value=10, max_value=100, value=resize_percent)
        quality = st.slider("Compression Quality", min_value=10, max_value=100, value=quality)

    # Compress image based on selected options
    st.write("🔄 Compressing...")
    resized_image = resize_image(image, resize_percent)
    compressed_image = compress_image(resized_image, quality)

    # Display compressed image
    st.image(compressed_image, caption=f"Compressed Image ({compression_level} Quality)", use_container_width=True)

    # Download button for the compressed image
    st.download_button(
        label="⬇️ Download Compressed Image",
        data=compressed_image,
        file_name="compressed_image.jpg",
        mime="image/jpeg"
    )

else:
    st.info("Please upload an image to compress.")
