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
import time

def resize_image(image, resize_percent):
    new_width = int(image.width * resize_percent / 100)
    new_height = int(image.height * resize_percent / 100)
    return image.resize((new_width, new_height))

def compress_image(image, quality):
    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=quality)
    buf.seek(0)
    return buf

# Add a progress bar during compression
def display_progress():
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.05)
        progress.progress(i + 1)

st.title("Enhanced Image Compressor")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_container_width=True)

    compression_level = st.slider("Choose Compression Level", min_value=10, max_value=100, value=70, help="Lower values lead to more compression but reduced image quality.")
    
    if st.button("Compress"):
        display_progress()

        resized_image = resize_image(image, 70)
        compressed_image = compress_image(resized_image, compression_level)

        st.image(compressed_image, caption="Compressed Image", use_container_width=True)
        
        # Download button
        st.download_button(label="⬇️ Download Compressed Image", data=compressed_image, file_name="compressed_image.jpg", mime="image/jpeg")
