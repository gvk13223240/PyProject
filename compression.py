import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="Simple Image Compressor", page_icon="🗜️")
st.title("🗜️ Simple Image Compressor")
st.write("by gvk13223240")

# Upload the image
uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

# Define compression presets
compression_presets = {
    "Low": {"resize": 0.3, "quality": 50},
    "Medium": {"resize": 0.5, "quality": 70},
    "High": {"resize": 0.7, "quality": 90}
}

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="🖼️ Original Image", use_container_width=True)

    # Get original size
    original_buf = io.BytesIO()
    image.save(original_buf, format="JPEG")
    original_size_kb = len(original_buf.getvalue()) / 1024

    st.write(f"📏 Original Image Size: **{original_size_kb:.2f} KB**")

    st.write("### 🔧 Select Compression Preset")

    # Compute sizes for all options
    options_with_sizes = []
    for label, settings in compression_presets.items():
        # Resize
        new_dims = (
            int(image.width * settings["resize"]),
            int(image.height * settings["resize"])
        )
        resized = image.resize(new_dims)
        buf = io.BytesIO()
        resized.save(buf, format="JPEG", quality=settings["quality"])
        compressed_kb = len(buf.getvalue()) / 1024
        options_with_sizes.append(f"{label} (~{compressed_kb:.1f} KB)")

    selected_option = st.selectbox("Choose Compression Level", options_with_sizes)
    selected_key = selected_option.split(" ")[0]  # "Low", "Medium", or "High"

    # Apply compression
    settings = compression_presets[selected_key]
    new_size = (
        int(image.width * settings["resize"]),
        int(image.height * settings["resize"])
    )
    compressed_image = image.resize(new_size)

    # Save and show
    compressed_buf = io.BytesIO()
    compressed_image.save(compressed_buf, format="JPEG", quality=settings["quality"])
    compressed_buf.seek(0)
    compressed_size_kb = len(compressed_buf.getvalue()) / 1024

    st.image(compressed_image, caption=f" Compressed Image - {selected_key}", use_container_width=True)
    st.success(f"✅ Compressed Size: **{compressed_size_kb:.2f} KB**")

    # Download
    st.download_button(
        label="⬇️ Download Compressed Image",
        data=compressed_buf,
        file_name="compressed_image.jpg",
        mime="image/jpeg"
    )
