import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any
from pydantic import BaseModel

class chatResponse(BaseModel):
    message: str
    data: Dict[str, Any]

@dataclass
class Chatbot:
    name: str
    introduction: str
    info_gathering_prompts: List[str]
    additional_questions: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    chat_history: List[Dict[str, Any]] = field(default_factory=list)
    collected_info: Dict[str, str] = field(default_factory=dict) 

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "introduction": self.introduction,
            "info_gathering_prompts": self.info_gathering_prompts,
            "additional_questions": self.additional_questions,
            "created_at": self.created_at.isoformat(),
            "chat_history": self.chat_history,
            "collected_info": self.collected_info
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Chatbot':
        chatbot = cls(
            name=data["name"],
            introduction=data["introduction"],
            info_gathering_prompts=data["info_gathering_prompts"],
            additional_questions=data["additional_questions"],
            id=data["id"],
        )
        chatbot.created_at = datetime.fromisoformat(data["created_at"])
        chatbot.chat_history = data.get("chat_history", [])
        chatbot.collected_info = data.get("collected_info", {})
        return chatbot