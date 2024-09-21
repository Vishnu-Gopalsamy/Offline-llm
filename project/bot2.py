import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

# Set up Streamlit app
st.set_page_config(page_title="Raghul's Chatbot", page_icon="🤖", layout="centered")
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

st.title("🤖 Raghul's AI Assistant")
st.subheader("Your Personal Chatbot Assistant")
st.write("Ask me anything, and I'll be happy to assist you!")

# Create columns for layout
col1, col2 = st.columns([1, 2])

# Use an expander for instructions
with st.expander("Click here for instructions"):
    st.write("""
        1. Enter your query in the text box below.
        2. Click on the **Submit** button to get the response.
        3. Feel free to ask any questions, and Raghul's Assistant will provide the answers!
    """)

# User input in the first column with centered image
with col1:
    st.markdown('<img src="https://tse4.mm.bing.net/th?id=OIP.Ol7oIrNn6w020SV2VNEUlAHaF5&pid=Api&P=0&h=180" class="center-img" width="200">', unsafe_allow_html=True)
    
input_txt = st.text_input("Please enter your queries here...")

# Initialize components
prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a helpful AI assistant. Your name is Raghul's Assistant."),
     ("user", "user query: {query}")]
)

llm = Ollama(model="llama2")
output_parser = StrOutputParser()

chain = prompt | llm | output_parser

# Button for submitting the query
if st.button("Submit"):
    if input_txt:
        # Call the LLM chain to get the response
        response = chain.invoke({"query": input_txt})
        # Show response in the second column
        with col2:
            st.markdown("### Response:")
            st.markdown(f"<div class='stMarkdown'>{response}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter a query before submitting!")
