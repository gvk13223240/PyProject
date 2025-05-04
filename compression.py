# import streamlit as st
# from PIL import Image
# import io

# st.set_page_config(page_title="Simple Image Compressor", page_icon="🗜️")
# st.title("🗜️ Simple Image Compressor")
# st.write("by gvk13223240")

# # Upload the image
# uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

# # Define compression presets
# compression_presets = {
#     "Low": {"resize": 0.3, "quality": 50},
#     "Medium": {"resize": 0.5, "quality": 70},
#     "High": {"resize": 0.7, "quality": 90}
# }

# if uploaded_file:
#     image = Image.open(uploaded_file).convert("RGB")
#     st.image(image, caption="🖼️ Original Image", use_container_width=True)

#     # Get original size
#     original_buf = io.BytesIO()
#     image.save(original_buf, format="JPEG")
#     original_size_kb = len(original_buf.getvalue()) / 1024

#     st.write(f"📏 Original Image Size: **{original_size_kb:.2f} KB**")

#     st.write("### 🔧 Select Compression Preset")

#     # Compute sizes for all options
#     options_with_sizes = []
#     for label, settings in compression_presets.items():
#         # Resize
#         new_dims = (
#             int(image.width * settings["resize"]),
#             int(image.height * settings["resize"])
#         )
#         resized = image.resize(new_dims)
#         buf = io.BytesIO()
#         resized.save(buf, format="JPEG", quality=settings["quality"])
#         compressed_kb = len(buf.getvalue()) / 1024
#         options_with_sizes.append(f"{label} (~{compressed_kb:.1f} KB)")

#     selected_option = st.selectbox("Choose Compression Level", options_with_sizes)
#     selected_key = selected_option.split(" ")[0]  # "Low", "Medium", or "High"

#     # Apply compression
#     settings = compression_presets[selected_key]
#     new_size = (
#         int(image.width * settings["resize"]),
#         int(image.height * settings["resize"])
#     )
#     compressed_image = image.resize(new_size)

#     # Save and show
#     compressed_buf = io.BytesIO()
#     compressed_image.save(compressed_buf, format="JPEG", quality=settings["quality"])
#     compressed_buf.seek(0)
#     compressed_size_kb = len(compressed_buf.getvalue()) / 1024

#     st.image(compressed_image, caption=f" Compressed Image - {selected_key}", use_container_width=True)
#     st.success(f"✅ Compressed Size: **{compressed_size_kb:.2f} KB**")

#     # Download
#     st.download_button(
#         label="⬇️ Download Compressed Image",
#         data=compressed_buf,
#         file_name="compressed_image.jpg",
#         mime="image/jpeg"
#     )
import streamlit as st
from PIL import Image
import io
import zipfile
import os

st.set_page_config(page_title="Advanced Image Compressor", page_icon="🗜️")
st.title("🗜️ Advanced Image Compressor")
st.write("by gvk13223240")

uploaded_files = st.file_uploader("📤 Upload image(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    st.subheader("🔧 Compression Settings")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        resize_percent = st.slider("Resize (%)", 10, 100, 50, step=5)
    with col2:
        quality = st.slider("Quality", 10, 100, 70, step=5)
    with col3:
        output_format = st.selectbox("Output Format", ["JPEG", "PNG", "WebP"])

    # Quality badge
    badge = "🟥 Low"
    if quality >= 80:
        badge = "🟩 High"
    elif quality >= 60:
        badge = "🟨 Medium"
    st.markdown(f"**Quality Level:** {badge}")

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for uploaded_file in uploaded_files:
            try:
                image = Image.open(uploaded_file).convert("RGB")
                orig_width, orig_height = image.size
                orig_buf = io.BytesIO()
                image.save(orig_buf, format="JPEG")
                original_size_kb = len(orig_buf.getvalue()) / 1024

                new_width = int(orig_width * resize_percent / 100)
                new_height = int(orig_height * resize_percent / 100)

                with st.spinner(f"Compressing {uploaded_file.name}..."):
                    resized_image = image.resize((new_width, new_height))
                    buf = io.BytesIO()
                    save_format = output_format.upper()
                    ext = save_format.lower()
                    if save_format == "JPG":
                        save_format = "JPEG"
                        ext = "jpg"
                    resized_image.save(buf, format=save_format, quality=quality)
                    buf.seek(0)
                    compressed_size_kb = len(buf.getvalue()) / 1024
                    reduction = 100 - (compressed_size_kb / original_size_kb * 100)

                    # Show comparison
                    st.markdown(f"### 🖼️ {uploaded_file.name}")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(image, caption=f"Original ({orig_width}×{orig_height}) - {original_size_kb:.2f} KB", use_container_width=True)
                    with col2:
                        st.image(resized_image, caption=f"Compressed ({new_width}×{new_height}) - {compressed_size_kb:.2f} KB", use_container_width=True)
                    
                    st.success(f"📉 Saved {reduction:.1f}% | Output: {compressed_size_kb:.2f} KB")

                    # Add to ZIP
                    zipf.writestr(f"{os.path.splitext(uploaded_file.name)[0]}.{ext}", buf.getvalue())

            except Exception as e:
                st.error(f"❌ Failed to process {uploaded_file.name}: {e}")

    zip_buffer.seek(0)
    st.download_button(
        label="⬇️ Download All Compressed Images (ZIP)",
        data=zip_buffer,
        file_name="compressed_images.zip",
        mime="application/zip"
    )
else:
    st.info("Upload one or more images to get started.")

