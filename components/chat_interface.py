import streamlit as st
from services.chatbot_service import get_chatbot_by_id, update_chatbot
import time
from services.chat_service import process_message, initialize_chat


def render_chat_interface():
    st.session_state.hide_main_title = True

    chatbot_id = st.session_state.selected_chatbot_id
    chatbot = get_chatbot_by_id(chatbot_id)

    if not chatbot:
        st.error("Chatbot not found!")
        if st.button("Back to List"):
            st.session_state.selected_chatbot_id = None
            st.rerun()
        return
    
    st.markdown("""
    <style>
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
    }
    .header-title {
        flex-grow: 1;
        text-align: center;
        margin: 0;
    }
    .button-container {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 8, 1])

    with col1:
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        if st.button("←", use_container_width=True):
            st.session_state.selected_chatbot_id = None
            st.session_state.hide_main_title = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<h1 class="header-title">Chat with {chatbot.name}</h1>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        if st.button("🔄 Reset", use_container_width=True, help="Reset chat history and collected data"):
            chatbot.chat_history = []
            chatbot.collected_info = {}
            
            initialize_chat(chatbot)
            
            if f"chat_initialized_{chatbot_id}" in st.session_state:
                del st.session_state[f"chat_initialized_{chatbot_id}"]
            
            update_chatbot(chatbot)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("")

    if f"chat_initialized_{chatbot_id}" not in st.session_state:
        initialize_chat(chatbot)
        st.session_state[f"chat_initialized_{chatbot_id}"] = True

    message_container = st.container(height=500, border=False)
    with message_container:
        for message in chatbot.chat_history:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    user_input = st.chat_input("Type your message here...")
    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            response = process_message(chatbot, user_input)

            full_response = ""
            for chunk in response.split():
                full_response += chunk + " "
                response_placeholder.markdown(full_response + "▌")
                st.session_state.typing = True
                time.sleep(0.05)

            response_placeholder.markdown(response)
            st.session_state.typing = False

    if chatbot.collected_info:
        with st.expander("📋 Collected Information"):
            for key, value in chatbot.collected_info.items():
                st.write(f"**{key}:** {value}")