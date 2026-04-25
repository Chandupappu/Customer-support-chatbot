import streamlit as st

st.title("🤖 Customer Support Chatbot")

user_input = st.text_input("Ask something:")

if user_input:
    st.write("You:", user_input)
    st.write("Bot: Working fine ✅")