from enum import Enum

class ToolMemoryKeys(Enum):
    TELEGRAM_MESSAGE_CONTENT = "telegram_message_content"
    ARTICLE_SEARCH_INPUT = "article_search_input"

class ToolMemory:
    def __init__(self):
        self.storage = {}

    def remember(self, key: str, value: str):
        self.storage[key] = value

    def recall(self, key: str) -> str:
        return self.storage.get(key, "")

memory = ToolMemory()
