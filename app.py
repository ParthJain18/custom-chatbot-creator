import streamlit as st
from components.sidebar import render_sidebar
from components.chatbot_creation import render_chatbot_creation_button, render_chatbot_creation_page
from components.chatbot_list import render_chatbot_list
from components.chat_interface import render_chat_interface
from utils.session import initialize_session


def main():
    st.set_page_config(page_title="Chatbot Creator", page_icon="🤖", layout="wide")

    initialize_session()
    
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    
    if 'hide_main_title' not in st.session_state:
        st.session_state.hide_main_title = False

    render_sidebar()

    if st.session_state.page == "create_chatbot":
        render_chatbot_creation_page()
    elif st.session_state.get('selected_chatbot_id'):
        if not st.session_state.hide_main_title:
            st.title("🤖 Chatbot Creator")
        render_chat_interface()
    else:
        st.title("🤖 Chatbot Creator")
        st.subheader("Create Your Own Chatbot")
        render_chatbot_creation_button()
        st.divider()
        st.subheader("Your Chatbots")
        render_chatbot_list()


if __name__ == "__main__":
    main()