import streamlit as st
from models.chatbot import Chatbot
from utils.storage import save_data, load_data
from typing import List, Optional


def get_all_chatbots() -> List[Chatbot]:
    chatbots_data = load_data("chatbots.json")
    return [Chatbot.from_dict(data) for data in chatbots_data]


def get_chatbot_by_id(chatbot_id: str) -> Optional[Chatbot]:
    chatbots = get_all_chatbots()
    for chatbot in chatbots:
        if chatbot.id == chatbot_id:
            return chatbot
    return None


def add_chatbot(chatbot: Chatbot) -> None:
    chatbots = get_all_chatbots()
    chatbots.append(chatbot)
    _save_chatbots(chatbots)


def update_chatbot(chatbot: Chatbot) -> None:
    chatbots = get_all_chatbots()
    for i, existing_chatbot in enumerate(chatbots):
        if existing_chatbot.id == chatbot.id:
            chatbots[i] = chatbot
            break
    _save_chatbots(chatbots)


def delete_chatbot(chatbot_id: str) -> None:
    chatbots = get_all_chatbots()
    chatbots = [chatbot for chatbot in chatbots if chatbot.id != chatbot_id]
    _save_chatbots(chatbots)

    if st.session_state.get('selected_chatbot_id') == chatbot_id:
        st.session_state.selected_chatbot_id = None


def _save_chatbots(chatbots: List[Chatbot]) -> None:
    chatbots_data = [chatbot.to_dict() for chatbot in chatbots]
    save_data("chatbots.json", chatbots_data)
