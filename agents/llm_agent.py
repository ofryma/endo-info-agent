import json    
import re
from typing import List

from colorama import Back, Fore, Style
from langchain_ollama import ChatOllama

from utils.stt import SpeakingCallbackHandler
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate
from langchain.tools import Tool
from langchain.callbacks.manager import CallbackManager
from langchain.output_parsers import PydanticOutputParser
from agents.models.response import AgentResult
from langchain.memory import ConversationBufferMemory

class LLMAgent:

    def __init__(self, model: str = 'llama2', *, tools: List[Tool] = [], callback_manager: CallbackManager = None , verbose: bool = False):
        # Initialize the callback handler with text-to-speech
        # self.callback_handler = SpeakingCallbackHandler()
        # if callback_manager is None:
        #     callback_manager = CallbackManager([self.callback_handler])

        # Initialize the LLM with Ollama
        self.llm = ChatOllama(
            model=model,
            temperature=0,
            callback_manager=callback_manager,
            verbose=verbose,
        )
        
        # Define tools the agent can use
        self.tools = tools
        
        self.memory = ConversationBufferMemory(return_messages=True)

        # Create the prompt template
        self.output_parser = PydanticOutputParser(pydantic_object=AgentResult)

        with open('agents/system_prompt_template.txt', 'r') as f:
            system_prompt_template = f.read()
        with open('agents/user_prompt_template.txt', 'r') as f:
            user_prompt_template = f.read()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt_template),
            ("user", user_prompt_template),
            ("placeholder", "{agent_scratchpad}")
        ]).partial(format_instructions=self.output_parser.get_format_instructions())

        # Create the agent using ReAct format
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt,
        )

        # Create the agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10,
            return_intermediate_steps=True,
        )

    def extract_json(self, text: str) -> str:
        try:
            json_match = re.search(r"\{.*\}", text, re.DOTALL)
            if json_match:
                return json_match.group()
        except Exception as e:
            print("Error during JSON extraction:", e)
        return None

    def agent_print(self, message: str):
        print(Fore.YELLOW + f"{message}\n" + Style.RESET_ALL)

    def run(self, input_text: str) -> AgentResult:
        """
        Run the agent with the given input text.
        
        Args:
            input_text (str): The input text to process
            
        Returns:
            AgentResult: The agent's response
        """

        try:
            result = self.agent_executor.invoke({"input": input_text})
            
            structured_result = self.output_parser.parse(self.extract_json(result.get('output')))
            return structured_result
        
        except Exception as e:
            error_message = f"Error: {str(e)}"
            return error_message