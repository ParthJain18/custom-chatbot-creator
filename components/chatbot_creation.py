import streamlit as st
from models.chatbot import Chatbot
from services.chatbot_service import add_chatbot


def render_chatbot_creation_button():
    if st.button("➕ Create New Chatbot", type="primary"):
        st.session_state.page = "create_chatbot"
        st.rerun()


def render_chatbot_creation_page():
    st.title("Create a New Chatbot")
    
    if st.button("← Back", key="back_btn"):
        st.session_state.page = "home"
        st.rerun()
    
    with st.form(key="chatbot_creation_form", border=False):
        name = st.text_input(
            "Chatbot Name", placeholder="Give your chatbot a name")

        introduction = st.text_area(
            "Introduction",
            placeholder="How would you like the chatbot to introduce itself?",
            height=100
        )

        st.markdown("##### Information Gathering")
        st.caption("Enter comma-separated values that the chatbot should collect from users.")
        st.caption("Example: Name, Age, Location, Profession")
        
        info_gathering = st.text_area(
            label="",
            placeholder='Enter values separated by commas (e.g., "Name", "Age", "Location")',
            height=100
        )
        
        if info_gathering:
            parsed_values = [item.strip().strip('"\'') for item in info_gathering.split(',') if item.strip()]
            
            if parsed_values:
                st.caption("Preview of data points to collect:")
                for i, value in enumerate(parsed_values, 1):
                    st.caption(f"{i}. {value}")

        additional_questions = st.text_area(
            "Additional Questions",
            placeholder="Any specific questions the chatbot should ask (e.g., about user's skillset)?",
            height=150
        )

        col1, col2 = st.columns([1, 4])

        with col1:
            submit = st.form_submit_button(
                "Create", type="primary", use_container_width=True)
        with col2:
            cancel = st.form_submit_button(
                "Cancel", type="secondary", use_container_width=False)

        if submit:
            if name and introduction:
                info_gathering_list = []
                if info_gathering:
                    info_gathering_list = [item.strip().strip('"\'') for item in info_gathering.split(',') if item.strip()]
                
                new_chatbot = Chatbot(
                    name=name,
                    introduction=introduction,
                    info_gathering_prompts=info_gathering_list,
                    additional_questions=additional_questions
                )

                add_chatbot(new_chatbot)

                st.session_state.page = "home"
                st.success(f"Chatbot '{name}' created successfully!")
                st.rerun()
            else:
                st.error(
                    "Please provide at least a name and introduction for your chatbot.")

        if cancel:
            st.session_state.page = "home"
            st.rerun()