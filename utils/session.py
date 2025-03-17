import streamlit as st

def initialize_session():
    if 'chatbots' not in st.session_state:
        st.session_state.chatbots = []
    
    if 'selected_chatbot_id' not in st.session_state:
        st.session_state.selected_chatbot_id = None
    
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    
    if 'hide_main_title' not in st.session_state:
        st.session_state.hide_main_title = False