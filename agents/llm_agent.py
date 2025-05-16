import json
from typing import List

from colorama import Back, Fore, Style
from langchain_ollama import ChatOllama

from utils.stt import SpeakingCallbackHandler
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate
from langchain.tools import Tool
from langchain.callbacks.manager import CallbackManager
from langchain.output_parsers import PydanticOutputParser
from tools.search import AgentResult
from tools.save import SaveTool


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
        self.tools = tools + [SaveTool()]

        # Create the prompt template
        self.output_parser = PydanticOutputParser(pydantic_object=AgentResult)

        with open('agents/prompt_template.txt', 'r') as f:
            prompt_template = f.read()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", prompt_template),
            ("placeholder", "{chat_history}"),
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}")
        ]).partial(format_instructions=self.output_parser.get_format_instructions())

        # Create the agent using ReAct format
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )

        # Create the agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
    
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
            result = self.agent_executor.invoke({"query": input_text})
            print(Fore.GREEN + "-"*50 + Style.RESET_ALL)
            print(result)
            print(Fore.GREEN + "-"*50 + Style.RESET_ALL)
            
            # Parse the result
            agent_result = AgentResult(**json.loads(result['output']))
            
            # Check if save was requested
            if "save" in input_text.lower():
                # Find the save tool
                save_tool = next((tool for tool in self.tools if tool.name == "save_to_file"), None)
                if save_tool:
                    save_result = save_tool.run(result['output'])
                    print(Fore.BLUE + f"\nSave result: {save_result}" + Style.RESET_ALL)
            
            return agent_result
        except Exception as e:
            error_message = f"Error: {str(e)}"
            return AgentResult(
                title="Error",
                description=error_message,
                tools_used=[]
            )
