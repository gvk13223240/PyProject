import streamlit as st 
import numpy as np
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Edge Detection (Sobel)", layout="wide")
st.markdown("<h1 style='text-align: center;'>🧠 Edge Detection using NumPy</h1>", unsafe_allow_html=True)
st.write("Created by - gvk13223240")

img = st.file_uploader("📤 Upload an Image", type=["png", "jpg", "jpeg"])

if img:
    try:
        image = Image.open(img).convert("RGB")
        st.image(image, caption="🖼️ Original Image", use_container_width=True)

        with st.spinner("Converting to Grayscale..."):
            grayscale_image = image.convert("L")
            st.image(grayscale_image, caption="📎 Grayscale Image", use_container_width=True)

        gray_np = np.array(grayscale_image, dtype='int32')

        sobel_x = np.array([[-1, 0, 1],
                            [-2, 0, 2],
                            [-1, 0, 1]])

        sobel_y = np.array([[-1, -2, -1],
                            [ 0,  0,  0],
                            [ 1,  2,  1]])

        def convolve2d(image, kernel):
            h, w = image.shape
            kh, kw = kernel.shape
            pad_h, pad_w = kh // 2, kw // 2
            padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
            output = np.zeros_like(image)
            for i in range(h):
                for j in range(w):
                    region = padded[i:i+kh, j:j+kw]
                    output[i, j] = np.sum(region * kernel)
            return output

        with st.spinner("🔍 Applying Sobel Edge Detection..."):
            gx = convolve2d(gray_np, sobel_x)
            gy = convolve2d(gray_np, sobel_y)

            edges = np.sqrt(gx**2 + gy**2)
            edges = np.clip(edges, 0, 255).astype('uint8')

            edge_img = Image.fromarray(edges)
            st.image(edge_img, caption="🧠 Sobel Edge Detection", use_container_width=True)

        buf = BytesIO()
        edge_img.save(buf, format="PNG")
        st.download_button("⬇️ Download Edge Image", buf.getvalue(), file_name="edge_detected.png")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
