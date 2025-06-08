import streamlit as st
from pptx import Presentation
from pptx.util import Inches
from PIL import Image
import io

layout_options = {
    "1 image per slide (1x1)": (1, 1),
    "2 images per slide (2x1)": (2, 1),
    "4 images per slide (2x2)": (2, 2),
    "6 images per slide (3x2)": (3, 2)
}

def screenshots_to_pptx_grid(image_files, layout, output_path="Screenshots_Presentation.pptx"):
    prs = Presentation()
    blank_layout = prs.slide_layouts[6]
    slide_width = prs.slide_width
    slide_height = prs.slide_height

    cols, rows = layout
    images_per_slide = cols * rows
    img_width = slide_width // cols
    img_height = slide_height // rows

    for i in range(0, len(image_files), images_per_slide):
        slide = prs.slides.add_slide(blank_layout)
        for j, image_file in enumerate(image_files[i:i + images_per_slide]):
            img = Image.open(image_file)
            image_stream = io.BytesIO()
            img.save(image_stream, format="PNG")
            image_stream.seek(0)

            col = j % cols
            row = j // cols
            left = col * img_width
            top = row * img_height

            slide.shapes.add_picture(image_stream, left, top, width=img_width, height=img_height)

    prs.save(output_path)

# Streamlit UI
st.set_page_config(page_title="Images to PPTX Converter", layout="centered")

st.title("📸 Images to PPTX Converter")

selected_layout = st.selectbox("Choose layout per slide", list(layout_options.keys()))
layout = layout_options[selected_layout]

uploaded_files = st.file_uploader(
    "Upload your images (PNG, JPG, JPEG)", 
    accept_multiple_files=True, 
    type=['png', 'jpg', 'jpeg']
)

if uploaded_files:
    st.image([Image.open(file) for file in uploaded_files], width=150, caption=[file.name for file in uploaded_files])
    
    if st.button("Generate PPTX"):
        screenshots_to_pptx_grid(uploaded_files, layout)
        with open("Screenshots_Presentation.pptx", "rb") as f:
            st.download_button(
                label="📥 Download Presentation",
                data=f,
                file_name="Screenshots_Presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
        st.success("✅ PPTX created successfully!")

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
