import streamlit as st
from PIL import Image
import numpy as np
import io

st.title("🗜️ Simple Image Compressor")
st.write("Created by: gvk13223240")
# Taking img as input
uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_container_width=True)

    # Choosing the level of compression
    st.write("### 🔧 Select Compression Preset")
    compression_level = st.selectbox(
        "Choose Compression Level",
        ["High Compression", "Medium Compression", "Low Compression"]
    )

    # setting the parameters for resize
    if compression_level == "High Compression":
        resize_percent = 30
        quality = 50
    elif compression_level == "Medium Compression":
        resize_percent = 50
        quality = 70
    elif compression_level == "Low Compression":
        resize_percent = 70
        quality = 90

    # Numpy resizing 
    image_array = np.array(image)  
    new_width = int(image.width * resize_percent / 100)
    new_height = int(image.height * resize_percent / 100)

    resized_image_array = np.array(Image.fromarray(image_array).resize((new_width, new_height), resample=Image.LANCZOS))
    
    resized_image = Image.fromarray(resized_image_array)

    # Displaying resized img
    st.image(resized_image, caption=f"Compressed Image ({compression_level})", use_container_width=True)

    # Saving the resized image
    buf = io.BytesIO()
    resized_image.save(buf, format="JPEG", quality=quality)
    buf.seek(0)

    # download button
    st.download_button(
        label="⬇️ Download Compressed Image",
        data=buf,
        file_name="compressed_image.jpg",
        mime="image/jpeg"
    )
