import streamlit as st
from pptx import Presentation
from pptx.util import Inches, Pt
from PIL import Image
import io

def screenshots_to_pptx_from_memory(image_files, output_path="Screenshots_Presentation.pptx"):
    prs = Presentation()
    blank_layout = prs.slide_layouts[6]

    for image_file in image_files:
        img = Image.open(image_file)
        img_width_px, img_height_px = img.size
        dpi = img.info.get("dpi", (96, 96))
        dpi_x = dpi[0] if dpi[0] else 96
        dpi_y = dpi[1] if dpi[1] else 96

        width_inches = img_width_px / dpi_x
        height_inches = img_height_px / dpi_y

        slide = prs.slides.add_slide(blank_layout)

        slide_width = prs.slide_width.inches
        slide_height = prs.slide_height.inches

        img_ratio = width_inches / height_inches
        slide_ratio = slide_width / slide_height

        if img_ratio > slide_ratio:
            pic_width = slide_width
            pic_height = slide_width / img_ratio
        else:
            pic_height = slide_height
            pic_width = slide_height * img_ratio

        image_stream = io.BytesIO()
        img.save(image_stream, format="PNG")
        image_stream.seek(0)

        slide.shapes.add_picture(
            image_stream,
            left=Inches((slide_width - pic_width) / 2),
            top=Inches((slide_height - pic_height) / 2),
            width=Inches(pic_width),
            height=Inches(pic_height),
        )

    prs.save(output_path)

st.title("📸 Images to PPTX Converter")

uploaded_files = st.file_uploader("Upload images", accept_multiple_files=True, type=['png','jpg','jpeg'])

if uploaded_files:
    st.image([Image.open(file) for file in uploaded_files], width=200, caption=[file.name for file in uploaded_files])
    if st.button("Generate PPTX"):
        screenshots_to_pptx_from_memory(uploaded_files)
        with open("Screenshots_Presentation.pptx", "rb") as f:
            st.download_button(
                label="Download PPTX",
                data=f,
                file_name="Screenshots_Presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
        st.success("PPTX file generated successfully!")
        st.balloons()

st.markdown(
    """
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
        background-color: #f0f2f6;
    }
    </style>
    <div class="footer">
        &copy; 2025 Vamshi Krishna G. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)
