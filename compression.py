import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="Image Compression App", layout="centered")

st.title("Image Compression App")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "bmp", "tiff", "tif", "webp", "gif"])

if uploaded_file is not None:
    filename = uploaded_file.name
    ext = os.path.splitext(filename)[1].lower()
    allowed_exts = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp", ".gif"]

    if ext in allowed_exts:
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image", use_column_width=True)

        quality = st.slider("Select Compression Quality (for JPG/JPEG/WebP)", min_value=1, max_value=95, value=60)

        if st.button("Compress"):
            compressed_path = f"compressed{ext}"
            format_map = {
                ".jpg": "JPEG",
                ".jpeg": "JPEG",
                ".webp": "WEBP",
                ".png": "PNG",
                ".bmp": "BMP",
                ".tiff": "TIFF",
                ".tif": "TIFF"
            }
            image_format = format_map.get(ext, "JPEG")

            if ext in [".jpg", ".jpeg", ".webp"]:
                image.save(compressed_path, format=image_format, optimize=True, quality=quality)
            else:
                image.save(compressed_path, format=image_format)

            st.success("Compression completed.")
            with open(compressed_path, "rb") as f:
                st.download_button("Download Compressed Image", f, file_name=compressed_path)
    else:
        st.error(f"Invalid file extension: {ext}. Allowed types are: {', '.join(allowed_exts)}")
