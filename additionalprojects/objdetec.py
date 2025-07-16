import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import cv2
from io import BytesIO

st.set_page_config(page_title="Basic Object Detection", layout="wide")

st.markdown("<h1 style='text-align: center;'>🔍 Basic Object Detection & Segmentation</h1>", unsafe_allow_html=True)
st.write("Created by - gvk13223240")

img = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

if img:
    # Load the image
    image = Image.open(img).convert("RGB")
    st.image(image, caption="Original Image", use_container_width=True)

    # Convert the image to grayscale
    grayscale_image = image.convert("L")
    st.image(grayscale_image, caption="Grayscale Image", use_container_width=True)

    # Convert PIL image to OpenCV format (numpy array)
    img_np = np.array(grayscale_image)

    # Apply binary thresholding
    _, thresholded = cv2.threshold(img_np, 127, 255, cv2.THRESH_BINARY)
    thresholded_image = Image.fromarray(thresholded)

    # Find contours
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_contour = np.array(image)

    # Draw contours on the original image
    cv2.drawContours(img_contour, contours, -1, (0, 255, 0), 3)

    # Convert the result back to PIL Image for display
    img_contour = Image.fromarray(img_contour)
    st.image(img_contour, caption="Detected Contours", use_container_width=True)

    # Label the contours
    labeled_img = np.array(image)
    for i, contour in enumerate(contours):
        cv2.drawContours(labeled_img, [contour], -1, (0, 0, 255), 2)
        # Put a label for each contour
        x, y, w, h = cv2.boundingRect(contour)
        cv2.putText(labeled_img, f"Object {i+1}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    labeled_img = Image.fromarray(labeled_img)
    st.image(labeled_img, caption="Labeled Objects", use_container_width=True)

    # Option to download the processed image
    buf = BytesIO()
    labeled_img.save(buf, format="PNG")
    st.download_button("Download Labeled Image", buf.getvalue(), file_name="labeled_image.png")
