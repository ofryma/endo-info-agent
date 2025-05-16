import wikipedia
from pydantic import BaseModel, Field, field_validator
from duckduckgo_search import DDGS
from scholarly import scholarly
from typing import List, Dict, Any
import json

from langchain_core.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun , WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from colorama import Fore, Back, Style

class AgentResult(BaseModel):
    """Model for agent results."""
    title: str = Field(..., description="The title of the result")
    description: str = Field(..., description="A brief description or summary of the result")
    tools_used: List[str] = Field(..., description="The tools used to get the result")

    @field_validator('tools_used')
    @classmethod
    def lowercase_tools(cls, v: List[str]) -> List[str]:
        return [tool.lower() for tool in v]

class AgentResponse(BaseModel):

    query: str = Field(..., description="The query to search for")
    output: str = Field(..., description="The output of the query")


def print_tool_usage(tool_name: str):
    """Print a formatted message when a tool is being used."""
    print(f"\n{Fore.CYAN}[Tool Usage] Using {tool_name}...{Style.RESET_ALL}\n")


wikipedia_api_wrapper = WikipediaAPIWrapper(
    top_k_results=1,
    doc_content_chars_max=1500
)

wikipedia_tool = WikipediaQueryRun(api_wrapper=wikipedia_api_wrapper)


search_web = DuckDuckGoSearchRun()
search_web_tool = Tool(
    name="search_web",
    description="Search the web using DuckDuckGo for information about a recent news article, or a specific topic or about latest trends and updates.",
    func=search_web.run
)

def search_google_scholar(query: str) -> str:
    """
    Search Google Scholar for academic articles and papers.
    
    Args:
        query (str): The search query
        
    Returns:
        str: A formatted string containing the search results
    """
    
    try:
        # Search for articles
        search_query = scholarly.search_pubs(query)
        
        # Get the first 3 results
        results = []
        for i in range(3):
            try:
                result = next(search_query)
                results.append(result)
            except StopIteration:
                break
        
        if not results:
            return json.dumps({"error": "No academic articles found for your query."})
        
        # Format the results
        formatted_results = []

        for result in results:
            title = result.get('bib', {}).get('title', 'No title')
            authors = result.get('bib', {}).get('author', ['Unknown authors'])
            year = result.get('bib', {}).get('pub_year', 'Unknown year')
            abstract = result.get('bib', {}).get('abstract', 'No abstract available')
            
            formatted_results.append(
                AgentResult(
                    title=title,
                    description=abstract,
                    sources=[f'{title} | {authors} | {year}']   
                )
            )

        return formatted_results[0].model_dump_json()
    
    except Exception as e:
        return json.dumps({"error": f"Error searching Google Scholar: {str(e)}"}) 
