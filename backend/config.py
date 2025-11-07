import os
import streamlit as st
import openai

# Global config
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not os.getenv("OPENAI_API_KEY"):
    st.error("OPENAI_API_KEY not set in environment variables!")
    st.stop()

# Constants (e.g., for scoring rules)
MAX_RESPONSE_TIME_SECONDS = 120
VERIFICATION_ELEMENTS = ['account_or_phone', 'name', 'address']