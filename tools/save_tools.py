import os
import json
from datetime import datetime

from colorama import Fore, Style
from pydantic import Field
from langchain.tools import BaseTool , tool

from agents.models.response import AgentResult
from tools import tools_memory

@tool()
def save_file(content: str) -> str:
    
    """
    Save the content to a text file.
    """

    content = tools_memory.memory.recall(tools_memory.ToolMemoryKeys.ARTICLE_SEARCH_INPUT.value)
    
    output_dir = os.path.join("outputs")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"query_result_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return f"Successfully saved results to {filepath}"

