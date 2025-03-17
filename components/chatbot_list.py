import streamlit as st
import time
from services.chatbot_service import get_all_chatbots, delete_chatbot


def render_chatbot_list():
    chatbots = get_all_chatbots()

    if not chatbots:
        st.info(
            "You haven't created any chatbots yet. Use the form above to create one!")
        return

    cols = st.columns(3)

    for i, chatbot in enumerate(chatbots):
        with cols[i % 3]:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.subheader(chatbot.name)

                with col2:
                    if st.button("🗑️", key=f"delete_{chatbot.id}", help="Delete this chatbot"):
                        st.session_state[f"confirm_delete_{chatbot.id}"] = True

                intro_preview = chatbot.introduction[:100] + "..." if len(
                    chatbot.introduction) > 100 else chatbot.introduction
                st.write(intro_preview)

                if st.button("💬 Chat", key=f"chat_{chatbot.id}"):
                    st.session_state.selected_chatbot_id = chatbot.id
                    st.rerun()

                if st.session_state.get(f"confirm_delete_{chatbot.id}", False):
                    st.warning("Are you sure you want to delete this chatbot?")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Yes", key=f"confirm_yes_{chatbot.id}"):
                            delete_chatbot(chatbot.id)
                            st.session_state.pop(
                                f"confirm_delete_{chatbot.id}", None)
                            st.rerun()
                    with col2:
                        if st.button("No", key=f"confirm_no_{chatbot.id}"):
                            st.session_state.pop(
                                f"confirm_delete_{chatbot.id}", None)
                            st.rerun()
