import streamlit as st
import requests
import os

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8080/api/v1/generate")

st.set_page_config(
    page_title="Sinai Digital Center",
    layout="wide"
)

# Sidebar
st.sidebar.image("frontend/logo.jpg", use_container_width=True)

st.title("Sinai Digital Center")
st.markdown("""
**Strategic Digital Corridor 36** - AI-Powered Content Generation
This tool generates strategic content for LinkedIn, Policy Briefs, Investor Pitches, and more using Vertex AI RAG and GPT-5.1.
""")

# Conversation Starters
st.subheader("Start a Conversation")
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

selected_query = None

with col1:
    if st.button("What is Project SDC36?"):
        selected_query = "What is Project SDC36 , and why 36 ?"
with col2:
    if st.button("Lobby in U.S. Politics?"):
        selected_query = "Lobby in U.S. Politics?"
with col3:
    if st.button("What is Nimbos Project?"):
        selected_query = "What is Nimbos Project and what is that has to do with SDC36 ?"

with col4:
    if st.button("Avoid Gov Shutdown?"):
        selected_query = "How Project like SDC36 could have avoid the longest U.S Government shut down in the history ?"
with col5:
    if st.button("Three-Continent Gateway?"):
        selected_query = "Why SDC36 considered to be the Three-Continent Gateway?"
with col6:
    if st.button("Weakening Lobby Influence?"):
        selected_query = "How SDC36 project will weakening the Lobby strength and  influence on Tax Payers and U.S current administration?"

# Main Input
if selected_query:
    query = st.text_area("Enter your request or topic:", value=selected_query, height=150)
else:
    query = st.text_area("Enter your request or topic:", height=150, placeholder="e.g., Write a LinkedIn post about the new subsea cable partnership with Egypt.")

if st.button("Generate Content", type="primary") or selected_query:
    if not query:
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Analyzing audience and generating content..."):
            try:
                response = requests.post(API_URL, json={"query": query})
                if response.status_code == 200:
                    result = response.json()
                    st.success("Content Generated Successfully!")
                    st.markdown("### Output")
                    st.markdown(result)
                    
                    # Copy button (simulated)
                    st.code(result, language="markdown")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")

st.markdown("---")
st.markdown('<p style="color: black; font-weight: bold; font-size: 20px;">Powered by Gemini 3 Pro , Google Vertex AI , Google Cloud , OpenAI GPT-5.1</p>', unsafe_allow_html=True)
