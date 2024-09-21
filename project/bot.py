import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# Set up Streamlit app
st.set_page_config(page_title="Raghul's Chatbot & Image Summarizer", page_icon="🤖", layout="centered")
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stTextInput>div>div>input {
        border: 2px solid #4CAF50;
        border-radius: 10px;
        font-size: 16px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stMarkdown {
        color: #333333;
        font-size: 18px;
    }
    .center-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("🤖 Raghul's AI Assistant & Image Summarizer")
st.subheader("Your Personal Chatbot and Image Summarization Tool")
st.write("Ask a question or upload an image for summarization.")

# Create a tabbed layout for both functionalities
tab1, tab2 = st.tabs(["💬 Chatbot", "🖼️ Image Summarizer"])

# Chatbot functionality in the first tab
with tab1:
    st.write("### Chat with Raghul's Assistant")

    # User input
    input_txt = st.text_input("Please enter your queries here...")

    # Initialize components for chatbot
    prompt = ChatPromptTemplate.from_messages(
        [("system", "You are a helpful AI assistant. Your name is Raghul's Assistant."),
         ("user", "user query: {query}")]
    )

    llm = Ollama(model="llama2")
    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser

    # Button for submitting the text query
    if st.button("Submit Query"):
        if input_txt:
            # Call the LLM chain to get the response
            try:
                response = chain.invoke({"query": input_txt})
                # Show response
                st.markdown("### Response:")
                st.markdown(f"<div class='stMarkdown'>{response}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a query before submitting!")

# Image Summarization functionality in the second tab
with tab2:
    st.write("### Upload an Image for Summarization")

    # File uploader for image input
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Load image captioning model
        @st.cache_resource
        def load_model():
            processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            return processor, model

        with st.spinner("Loading model..."):
            processor, model = load_model()

        # Process the image for summarization
        inputs = processor(image, return_tensors="pt")

        # Generate the summary (caption)
        with st.spinner("Generating summary..."):
            try:
                out = model.generate(**inputs)
                summary = processor.decode(out[0], skip_special_tokens=True)
                # Display the summary
                st.write("### Summary:")
                st.write(summary)
            except Exception as e:
                st.error(f"An error occurred: {e}")
