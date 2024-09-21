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
    .main-container {
        background: linear-gradient(to bottom right, #4CAF50, #2196F3);
        padding: 20px;
        border: 5px solid #fff;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
    }
    .stTextInput>div>div>input {
        border: 2px solid #fff;
        border-radius: 10px;
        font-size: 16px;
        background-color: rgba(255, 255, 255, 0.8);
    }
    .stButton>button {
        background-color: #ff9800;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #e68a00;
    }
    .stMarkdown {
        color: #fff;
        font-size: 18px;
    }
    .center-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        border-radius: 15px;
    }
    .chat-history {
        background-color: rgba(255, 255, 255, 0.2);
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .chat-message {
        padding: 8px;
        background-color: rgba(255, 255, 255, 0.3);
        border-radius: 8px;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.title("🤖 Raghul's AI Assistant & Image Summarizer")
st.subheader("Your Personal Chatbot and Image Summarization Tool")
st.write("Ask a question or upload an image for summarization.")

# Create a tabbed layout for both functionalities
tab1, tab2, tab3 = st.tabs(["💬 Chatbot", "🖼️ Image Summarizer", "📝 History"])

# Chat history list and image summary history stored in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "image_history" not in st.session_state:
    st.session_state.image_history = []

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
                # Add the user query and response to the history
                st.session_state.chat_history.append(("User", input_txt))
                st.session_state.chat_history.append(("Assistant", response))

                # Display the chat history
                st.markdown("### Chat History:")
                for i, (sender, message) in enumerate(st.session_state.chat_history):
                    st.markdown(
                        f"<div class='chat-message'><b>{sender}:</b> {message}</div>",
                        unsafe_allow_html=True,
                    )
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

                # Save the image summary to history
                st.session_state.image_history.append((uploaded_file.name, summary))

            except Exception as e:
                st.error(f"An error occurred: {e}")

# History Tab
with tab3:
    st.write("### Previous Chat and Image Summarizations")

    # Display Chat History
    if st.session_state.chat_history:
        st.markdown("### Chat History:")
        for i, (sender, message) in enumerate(st.session_state.chat_history):
            st.markdown(
                f"<div class='chat-message'><b>{sender}:</b> {message}</div>",
                unsafe_allow_html=True,
            )
    else:
        st.write("No chat history available.")

    # Display Image Summarization History
    if st.session_state.image_history:
        st.markdown("### Image Summarization History:")
        for i, (img_name, summary) in enumerate(st.session_state.image_history):
            st.markdown(f"**Image**: {img_name}")
            st.markdown(f"**Summary**: {summary}")
    else:
        st.write("No image summary history available.")

st.markdown('</div>', unsafe_allow_html=True)
