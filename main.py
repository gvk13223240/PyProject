import streamlit as st
from pptx import Presentation
from pptx.util import Inches
from PIL import Image, ImageDraw
import io
import math

layout_options = {
    "1 image per slide (1x1)": (1, 1),
    "2 images per slide (2x1)": (2, 1),
    "4 images per slide (2x2)": (2, 2),
    "6 images per slide (3x2)": (3, 2)
}

def generate_pptx(image_files, layout, output_path="Screenshots_Presentation.pptx"):
    prs = Presentation()
    blank_layout = prs.slide_layouts[6]
    slide_width = prs.slide_width
    slide_height = prs.slide_height

    cols, rows = layout
    per_slide = cols * rows
    img_width = slide_width // cols
    img_height = slide_height // rows

    for i in range(0, len(image_files), per_slide):
        slide = prs.slides.add_slide(blank_layout)
        for j, image_file in enumerate(image_files[i:i+per_slide]):
            img = Image.open(image_file)
            image_stream = io.BytesIO()
            img.save(image_stream, format="PNG")
            image_stream.seek(0)
            col = j % cols
            row = j // cols
            slide.shapes.add_picture(image_stream, col * img_width, row * img_height, width=img_width, height=img_height)

    prs.save(output_path)

def create_slide_mockups(image_files, layout):
    slide_previews = []
    cols, rows = layout
    per_slide = cols * rows
    thumb_width, thumb_height = 200 * cols, 150 * rows
    box_w, box_h = thumb_width // cols, thumb_height // rows

    for i in range(0, len(image_files), per_slide):
        canvas = Image.new("RGB", (thumb_width, thumb_height), "white")
        for j, image_file in enumerate(image_files[i:i+per_slide]):
            thumb = Image.open(image_file).copy()
            thumb.thumbnail((box_w, box_h))
            x = (j % cols) * box_w
            y = (j // cols) * box_h
            canvas.paste(thumb, (x, y))
        slide_previews.append(canvas)
    return slide_previews

# Streamlit UI
st.set_page_config(page_title="PPT Generator", layout="centered")
st.title("📸 Images to PPTX Converter")

selected_layout = st.selectbox("Choose layout per slide", list(layout_options.keys()))
layout = layout_options[selected_layout]

uploaded_files = st.file_uploader("Upload images", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

# Show Generate Button at Top
if uploaded_files:
    if st.button("🚀 Generate PPTX"):
        generate_pptx(uploaded_files, layout)
        with open("Screenshots_Presentation.pptx", "rb") as f:
            st.download_button(
                label="📥 Download PPTX",
                data=f,
                file_name="Screenshots_Presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
        st.success("✅ PPTX generated successfully!")
        st.balloons()

    # Show Slide Mockup Previews
    st.subheader("🔍 Slide Preview")
    for idx, preview in enumerate(create_slide_mockups(uploaded_files, layout), 1):
        st.image(preview, caption=f"Slide {idx}", use_column_width=True)

# Footer
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        color: gray;
        font-size: 12px;
        padding: 10px 0;
    }
    </style>
    <div class="footer">
        &copy; 2025 Vamshi Krishna G. All rights reserved.
    </div>
""", unsafe_allow_html=True)
