from typing import List

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from colorama import Fore, Back, Style

from utils.stt import SpeakingCallbackHandler
from agents.llm_agent import LLMAgent

from tools.search import wikipedia_tool, search_web_tool
from utils.speech_recognition_util import SpeechRecognizer



# Load environment variables
load_dotenv()

TOOLS = [
    wikipedia_tool,
    # search_web_tool,
]


def main():
    
    # Initialize the agent
    agent = LLMAgent(
        model="llama3.1",
        tools=TOOLS,
        verbose=True
    )

    agent.agent_print("""
    Welcome! I'm your AI assistant. You can:
    - Type your message and press Enter
    - Just press Enter to use voice input
    - Type 'quit' to exit
    """)
    
    while True:
        print("\n" + "="*50)
        user_input = input(Fore.CYAN + "> ")

        print(Style.RESET_ALL + "\n" + "="*50)
        
        if user_input.lower() == 'quit':
            print(Fore.YELLOW + "\n👋 Goodbye!" + Style.RESET_ALL)
            break

        if not user_input.strip():
            # If user just pressed Enter, start voice input
            agent.agent_print(Fore.YELLOW + "\n🎤 Listening... (speak now)" + Style.RESET_ALL)
            user_input = SpeechRecognizer().listen_for_input()

            if not user_input:
                agent.agent_print("No speech detected. Please try again.")
                continue

        response = agent.run(user_input)

        if response.title == 'Error':
            agent.agent_print(Fore.RED + f"{response.title}: {response.description}\n")

        print(Style.RESET_ALL)

if __name__ == "__main__":
    main() 