import streamlit as st
import numpy as np
from PIL import Image
import io

st.title("🌈 Color Image Compressor using SVD")

uploaded_file = st.file_uploader("Upload a color image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_column_width=True)

    k = st.slider("Compression Level (Number of Singular Values)", min_value=5, max_value=min(image.size) - 1, value=50)

    if st.button("Compress"):
        st.write("🔄 Compressing using SVD...")

        # Convert image to NumPy array
        img_array = np.array(image, dtype=np.float64)
        compressed_channels = []

        # Apply SVD separately to R, G, B
        for i in range(3):  # R, G, B
            channel = img_array[:, :, i]
            U, S, Vt = np.linalg.svd(channel, full_matrices=False)
            S_k = np.diag(S[:k])
            U_k = U[:, :k]
            Vt_k = Vt[:k, :]
            compressed_channel = np.dot(U_k, np.dot(S_k, Vt_k))
            compressed_channel = np.clip(compressed_channel, 0, 255)
            compressed_channels.append(compressed_channel.astype(np.uint8))

        # Stack channels back into an image
        compressed_image = np.stack(compressed_channels, axis=2)
        final_image = Image.fromarray(compressed_image)

        st.image(final_image, caption=f"Compressed Image with k={k}", use_column_width=True)

        # Download button
        buf = io.BytesIO()
        final_image.save(buf, format="JPEG")
        buf.seek(0)
        st.download_button(
            label="⬇️ Download Compressed Image",
            data=buf,
            file_name="svd_compressed_color.jpg",
            mime="image/jpeg"
        )
