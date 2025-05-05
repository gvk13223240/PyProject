import streamlit as st
import numpy as np
from PIL import Image
import io
import hashlib

# Custom CSS to place login button at the top-right corner
st.markdown("""
    <style>
        .login-button {
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 9999;
        }
    </style>
""", unsafe_allow_html=True)

# Dummy authentication function (for demonstration)
def check_login(username, password):
    correct_username = "user"
    correct_password_hash = hashlib.sha256("password123".encode()).hexdigest()
    
    if username == correct_username and hashlib.sha256(password.encode()).hexdigest() == correct_password_hash:
        return True
    return False

# Function to display login form
def login():
    st.title("Login to Access Image Compressor")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if check_login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login Successful!")
        else:
            st.error("Invalid username or password.")

# If the user is logged in, show the image compressor
def image_compressor():
    st.title("Image Compressor")
    st.write("by gvk13223240")

    uploaded_file = st.file_uploader("Upload a color image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Original Image", use_container_width=True)

        k = st.slider("Compression Level (Number of Singular Values)", min_value=5, max_value=min(image.size) - 1, value=50)

        if st.button("Compress"):
            st.write("🔄 Compressing...")

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

            st.image(final_image, use_container_width=True)

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

# Check if the user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    login()
else:
    # If logged in, show the image compressor
    image_compressor()
