from colorama import Fore, Back, Style

from tools.search_tools import scholar_article_search , wikipedia_search
from tools.save_tools import save_file
from utils.stt import SpeakingCallbackHandler
from agents.llm_agent import LLMAgent
from utils.speech_recognition_util import SpeechRecognizer
from tools.telegram_tools import send_telegram_message
TOOLS = [
    scholar_article_search,
    wikipedia_search,
    save_file,
    send_telegram_message
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

        # user_input = "Research about machine learning. Save research content in a file."
        # print(Fore.CYAN + "> " + user_input)

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


        print("-"*50)
        agent.agent_print(response)
        print("-"*50)

        break

if __name__ == "__main__":
    main()