import streamlit as st
from PIL import Image
import numpy as np
import io

st.set_page_config(page_title="Simple Image Compressor", page_icon="🗜️")
st.title("🗜️ Simple Image Compressor")
st.write("by gvk13223240")

uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_container_width=True)

    st.write("### 🔧 Select Compression Preset")
    compression_level = st.selectbox(
        "Choose Compression Level",
        ["Low", "Medium", "High"]
    )

    if compression_level == "High":
        resize_percent = 30
        quality = 50
        quality_level="Low"
    elif compression_level == "Medium":
        resize_percent = 50
        quality = 70
        quality_level="Medium"
    elif compression_level == "Low":
        resize_percent = 70
        quality = 90
        quality_level="High"

    # Convert the image to a numpy array
    img_array = np.array(image)

    # Resize the image manually using numpy
    new_width = int(image.width * resize_percent / 100)
    new_height = int(image.height * resize_percent / 100)
    resized_img_array = np.array(Image.fromarray(img_array).resize((new_width, new_height)))

    # Convert numpy array back to PIL image
    resized_image = Image.fromarray(resized_img_array)

    # Save image in memory (JPEG format)
    buf = io.BytesIO()
    resized_image.save(buf, format="JPEG", quality=quality)
    buf.seek(0)

    compressed_size_kb = len(buf.getvalue()) / 1024

    # Display the resized and compressed image
    st.image(resized_image, caption=f"Compressed Image ({quality_level} Quality - {compressed_size_kb:.2f} KB)", use_container_width=True)

    # Download button for the compressed image
    st.download_button(
        label="⬇️ Download Compressed Image",
        data=buf,
        file_name="compressed_image.jpg",
        mime="image/jpeg"
    )
else:
    st.info("Please upload a JPG or PNG image to compress.")
