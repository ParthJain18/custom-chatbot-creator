from models.chatbot import Chatbot, chatResponse
from services.chatbot_service import update_chatbot
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def initialize_chat(chatbot: Chatbot):

    prompt = f"""
        You are {chatbot.name}. Your job is to collect data from the user regarding the given topics below in a natural way. You may infer some information from the user's chat or ask for the information directly.
        Information to gather: {chatbot.info_gathering_prompts}

        """

    prompt += """
        For your response, you must follow this json schema (The data fields would depend on the information you are collecting):
        And message would be passed as a response to the user.
        {{
            "message": "Hello, Parth! That was a wonderful introduction. Can you please provide me with your skillsets as well?",
            "data": {{
                "name": "Parth Jain",
                "age": 21,
                "location": "Mumbai",
                "profession": "Software Engineer"
            }}
        }}
        """
    
    if chatbot.additional_questions:
        prompt += f"Additionally, if you are done gathering all the required information, you may ask the user questions regarding: {chatbot.additional_questions}"

    if not chatbot.chat_history:
        chatbot.chat_history.append({
            "role": "system",
            "content": prompt,
        })
        chatbot.chat_history.append({
            "role": "assistant",
            "content": chatbot.introduction,
        })
        update_chatbot(chatbot)


def process_message(chatbot: Chatbot, message: str) -> str:
    chatbot.chat_history.append({
        "role": "user",
        "content": message,
    })

    response = generate_response(chatbot, message)

    chatbot.chat_history.append({
        "role": "assistant",
        "content": response,
    })

    update_chatbot(chatbot)

    return response


def generate_response(chatbot: Chatbot, message: str) -> str:

    retry = 0
    temp_chat_history = chatbot.chat_history.copy()

    collection_instructions = {
        "role": "system",
        "content": f"""
            Process the user's last message and update the collected information.
            Required information to gather: {chatbot.info_gathering_prompts}
            Current collected information: {str(chatbot.collected_info)}
            Return a JSON with the message and the data collected and if yuo're asking any addistional questions, make sure to track the user's response in the data field Just create a list of dict for "question" and "user_response" for additional questions stated in the system prompt earlier.
        """
    }
    
    temp_chat_history.append(collection_instructions)

    while (retry < 3):
        try:
            response = client.chat.completions.create(
                messages = temp_chat_history,
                model = "llama-3.3-70b-versatile",
                response_format={"type": "json_object"},
                stream=False
            ).choices[0].message.content

            validated_response = chatResponse.model_validate_json(response)
            chatbot.collected_info.update(validated_response.data)
            update_chatbot(chatbot)

            return validated_response.message
    
        
        except Exception as e:
            retry += 1
            print(e)
            print("Retrying...")
    
    
    return "I'm sorry. Some unexpected error occured. Please try again later."