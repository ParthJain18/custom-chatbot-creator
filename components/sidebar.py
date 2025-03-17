import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.title("🤖 Chatbot Creator")

        st.markdown("""
        ## About
        This application allows you to create custom chatbots with specific behaviors.
        
        ## How to use:
        1. Click "Create New Chatbot" button
        2. Fill in the configuration details
        3. Click on a chatbot to start chatting
        """)

        st.divider()

        if st.button("Home", key="home_btn", help="Go back to the home page", use_container_width=True):
            st.session_state.page = "home"
            st.session_state.selected_chatbot_id = None
            st.rerun()

        if st.button("New Chatbot", key="new_chatbot_btn", help="Create a new chatbot", use_container_width=True):
            st.session_state.page = "create_chatbot"
            st.rerun()