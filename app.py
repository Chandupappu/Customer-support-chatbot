import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------- Load data ----------
with open("data.txt", "r") as f:
    documents = [d.strip() for d in f.readlines() if d.strip()]

vectorizer = TfidfVectorizer()
doc_vectors = vectorizer.fit_transform(documents)

# ---------- 🔥 REPLACE THIS FUNCTION ----------
def get_response(user_input):
    text = user_input.lower().strip()

    # INTENTS
    if any(word in text for word in ["hi", "hello", "hey"]):
        return "Hello! How can I help you today? 😊"

    if "how are you" in text:
        return "I’m doing great! How can I assist you? 😊"

    if "thanks" in text or "thank you" in text:
        return "You're welcome! 🙌"

    if "support" in text or "help" in text:
        return "Support is available 24/7."

    # RAG
    user_vec = vectorizer.transform([text])
    sims = cosine_similarity(user_vec, doc_vectors)

    best_idx = sims.argmax()
    confidence = sims[0][best_idx]

    if confidence < 0.25:
        return "Sorry, I’m not sure. Please ask about orders, refunds, or payments."

    return documents[best_idx]


# ---------- UI ----------
st.set_page_config(page_title="Customer Support Chatbot")
st.title("🤖 Customer Support Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = get_response(user_input)

    st.session_state.messages.append({"role": "assistant", "content": response})

    st.rerun()