import streamlit as st
import requests
from PIL import Image

# Hugging Face Inference API
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
headers = {"Authorization": "Bearer YOUR_HUGGINGFACE_API_TOKEN"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

st.set_page_config(page_title="Image Summarizer", page_icon="🖼️", layout="centered")
st.title("🖼️ Image Summarizer")
st.write("Upload an image, and the system will generate a summary.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Save the image temporarily
    with open("temp_image.png", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Get the summary using the Hugging Face API
    with st.spinner("Generating summary..."):
        output = query("temp_image.png")
        summary = output.get("generated_text", "No summary available.")

    # Display the summary
    st.write("### Summary:")
    st.write(summary)
