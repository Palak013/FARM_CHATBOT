import streamlit as st
import google.generativeai as genai


genai.configure(api_key="Your API KEY")


model = genai.GenerativeModel(model_name="gemini-1.5-flash")


VALID_USERS = ["BHANU","PALAK"]


st.set_page_config(page_title="Farm Budget Chatbot", page_icon="🌾")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "messages" not in st.session_state:
    st.session_state.messages = []


if not st.session_state.authenticated:
    st.title("🔐 Welcome to Farm Budget Planner Chatbot")
    username = st.text_input("Enter your username:", key="login_user")

    if st.button("Login"):
        if username.strip().upper() in VALID_USERS:
            st.session_state.authenticated = True
            st.session_state.username = username.strip().capitalize()
            st.success(f"✅ Welcome, {st.session_state.username}!")
            st.rerun()
        else:
            st.error("❌ Access Denied. Invalid Username.")
else:
    
    st.title("🌾 Farm Budget Planner Chatbot")
    st.write(f"Hi **{st.session_state.username}**, ask me anything about farm budgeting.")

   
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.messages = []
        st.rerun()

   
    user_input = st.text_input("👨‍🌾 You:", key="user_input", placeholder="e.g., Budget for wheat on 2 acres")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("🤖 Thinking..."):
            try:
                response = model.generate_content(user_input)
                reply = response.text
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.session_state.messages.append({"role": "assistant", "content": f"Sorry, something went wrong: {e}"})

   
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"👨‍🌾 *You:* {msg['content']}")
        else:
            st.markdown(f"🤖 *Bot:* {msg['content']}")

