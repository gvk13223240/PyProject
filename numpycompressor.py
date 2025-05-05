import streamlit as st
from PIL import Image
import numpy as np
import io
import mimetypes
import time

st.set_page_config(page_title="Simple Image Compressor", page_icon="🗜️")
st.title("🗜️ Simple Image Compressor")
st.write("by gvk13223240")

uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Check MIME type and ensure it's a valid image type
    mime_type, encoding = mimetypes.guess_type(uploaded_file.name)
    
    if mime_type in ['image/jpeg', 'image/png']:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Original Image", use_container_width=True)

        # Display original image size in MB
        original_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        st.write(f"Original Image Size: {original_size_mb:.2f} MB")

        st.write("### 🔧 Select Compression Preset")
        compression_level = st.selectbox(
            "Choose Compression Level",
            ["Low", "Medium", "High"]
        )

        # Set resize and quality based on selected compression level
        if compression_level == "High":
            resize_percent = 30
            quality = 50
            quality_level = "Low"
        elif compression_level == "Medium":
            resize_percent = 50
            quality = 70
            quality_level = "Medium"
        elif compression_level == "Low":
            resize_percent = 70
            quality = 90
            quality_level = "High"

        # Convert the image to a numpy array
        img_array = np.array(image)

        # Resize logic
        new_width = int(image.width * resize_percent / 100)
        new_height = int(image.height * resize_percent / 100)
        resized_img_array = np.array(Image.fromarray(img_array).resize((new_width, new_height)))

        # Converting numpy array back to PIL image
        resized_image = Image.fromarray(resized_img_array)

        # Start compression animation
        with st.spinner("Compressing the image... Please wait!"):
            # Simulate compression delay
            time.sleep(2)

            # Save image in memory
            buf = io.BytesIO()
            resized_image.save(buf, format="JPEG", quality=quality)
            buf.seek(0)

            # Get the compressed size in MB
            compressed_size_mb = len(buf.getvalue()) / (1024 * 1024)

            # Display the result
            st.write(f"🔄 Compression completed! The compressed image size is {compressed_size_mb:.2f} MB.")
            st.image(resized_image, caption=f"Compressed Image ({quality_level} Quality - {compressed_size_mb:.2f} MB)", use_container_width=True)

            # Allow user to download the compressed image
            st.download_button(
                label="⬇️ Download Compressed Image",
                data=buf,
                file_name="compressed_image.jpg",
                mime="image/jpeg"
            )
    else:
        st.error("Please upload a valid JPG or PNG image.")
else:
    st.info("Please upload a JPG or PNG image to compress.")
