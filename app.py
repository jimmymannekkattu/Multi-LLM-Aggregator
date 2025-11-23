import streamlit as st
import asyncio
from llm_providers import get_all_responses
from offline_model import synthesize_responses

# Page Config
st.set_page_config(
    page_title="Multi-LLM Aggregator",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for "Premium" feel
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stTextArea textarea {
        background-color: #262730;
        color: #ffffff;
        border-radius: 10px;
    }
    .stButton button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 20px;
        padding: 10px 24px;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #ff6b6b;
    }
    .provider-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
        margin-bottom: 20px;
        height: 400px;
        overflow-y: auto;
    }
    .final-answer {
        background: linear-gradient(145deg, #1e1e1e, #2d2d2d);
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #444;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Multi-LLM Aggregator")
st.markdown("Ask one question. Get the combined wisdom of **ChatGPT, Claude, Gemini, and Perplexity**, synthesized by your local AI.")

# Input Section
with st.container():
    query = st.text_area("Enter your question here...", height=100)
    ask_button = st.button("🚀 Ask the Swarm")

if ask_button and query:
    status_container = st.empty()
    
    # Run async loop
    async def run_process():
        status_container.info("⏳ Querying online models (ChatGPT, Claude, Gemini, Perplexity)...")
        
        # 1. Fetch from all providers
        responses = await get_all_responses(query)
        
        status_container.success("✅ Responses received! Synthesizing final answer with local model...")
        
        # 2. Synthesize with offline model
        final_answer = await synthesize_responses(query, responses)
        
        status_container.empty()
        return responses, final_answer

    # Streamlit runs sync by default, so we use asyncio.run
    try:
        responses, final_answer = asyncio.run(run_process())
        
        # Display Final Answer
        st.markdown("### ✨ Synthesized Answer")
        st.markdown(f'<div class="final-answer">{final_answer}</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Display Individual Responses
        st.markdown("### 🧠 Individual Model Perspectives")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ChatGPT (OpenAI)")
            st.markdown(f'<div class="provider-card">{responses["ChatGPT"]}</div>', unsafe_allow_html=True)
            
            st.markdown("#### Gemini (Google)")
            st.markdown(f'<div class="provider-card">{responses["Gemini"]}</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown("#### Claude (Anthropic)")
            st.markdown(f'<div class="provider-card">{responses["Claude"]}</div>', unsafe_allow_html=True)
            
            st.markdown("#### Perplexity")
            st.markdown(f'<div class="provider-card">{responses["Perplexity"]}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

else:
    if ask_button:
        st.warning("Please enter a question first.")
