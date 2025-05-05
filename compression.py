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

def estimate_size(image, resize_percent, quality):
    new_width = int(image.width * resize_percent / 100)
    new_height = int(image.height * resize_percent / 100)
    estimated_size = (new_width * new_height * 3 * quality) / (100 * 1000)
    return estimated_size

st.set_page_config(page_title="Image Compressor", page_icon="🗜️")
st.title("🗜️ Simple Image Compressor")
st.write("Created by - gvk13223240")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_container_width=True)

    st.write("### Choose one of the following options for compression:")

    compression_level = st.radio(
        "Select a Compression Level:",
        ["Use Preset Compression (Low, Medium, High)", "Use Custom Compression Settings"]
    )

    if compression_level == "Use Preset Compression (Low, Medium, High)":
        st.write("You have selected the **Preset Compression** option.")
        preset_compression = st.selectbox(
            "Choose Compression Level",
            ["Low", "Medium", "High"]
        )

        if preset_compression == "High":
            resize_percent = 30
            quality = 50
            quality_level = "Low"
        elif preset_compression == "Medium":
            resize_percent = 50
            quality = 70
            quality_level = "Medium"
        elif preset_compression == "Low":
            resize_percent = 70
            quality = 90
            quality_level = "High"

        st.write(f"Compression Level: {preset_compression} ({resize_percent}% size, {quality}% quality)")

    else:
        st.write("You have selected the **Custom Compression Settings** option.")
        resize_percent = st.slider("Resize Percentage", min_value=10, max_value=100, value=50)
        quality = st.slider("Compression Quality", min_value=10, max_value=100, value=70)
        quality_level = f"{quality}% Quality"

    estimated_size_kb = estimate_size(image, resize_percent, quality)
    st.write("🔄 Compressing...")

    resized_image = resize_image(image, resize_percent)
    compressed_image = compress_image(resized_image, quality)

    st.image(compressed_image, caption=f"Compressed Image ({quality_level})", use_container_width=True)
    st.write(f"Estimated Compressed Size: {estimated_size_kb:.2f} KB")

    st.download_button(
        label="⬇️ Download Compressed Image",
        data=compressed_image,
        file_name="compressed_image.jpg",
        mime="image/jpeg"
    )
else:
    st.info("Please upload an image to compress.")
