import json
from typing import List
from datetime import datetime
from scholarly import scholarly
from langchain_core.tools import Tool, tool

from colorama import Fore, Back, Style
import wikipedia
from tools import tools_memory


def store_in_memory(content: str):
    print(Fore.YELLOW + f"Storing in memory: {content}")
    tools_memory.memory.remember(tools_memory.ToolMemoryKeys.ARTICLE_SEARCH_INPUT.value, content)
    tools_memory.memory.remember(tools_memory.ToolMemoryKeys.TELEGRAM_MESSAGE_CONTENT.value, content)

@tool
def wikipedia_search(input: str) -> str:
    """
    Search results about a given topic from Wikipedia.
    Use this tool to search for information about a given topic from Wikipedia, for static information that is not time-sensitive.
    """

    print(Fore.YELLOW + f"Searching Wikipedia about {input}...")

    summary = wikipedia.summary(input, auto_suggest=False)

    # Store the results in memory
    store_in_memory(summary)

    try:
        return summary
    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"

@tool
def scholar_article_search(input: str) -> str:
    """
    Search results about articles in the given field from Google Scholar.
    Use this tool to search for information about articles in the given field from Google Scholar, for time-sensitive information,
    or when you need to find the most recent articles.
    """

    current_year = datetime.now().year
    
    try:

        print(Fore.YELLOW + f"Searching Google Scholar about {input} between {current_year} and {current_year - 1}...")
        # Search Google Scholar for a single article
        search_query = scholarly.search_pubs(
            input , 
            year_high=current_year , 
            year_low=current_year - 1,
            sort_by="date",
            )
        
        print(f"Nice, there are {len(search_query)} results. Searching one matching the current year ({current_year})...")

        results = []
        for pub in search_query:
            if pub.get('bib', {}).get('pub_year', '') == current_year:
                results.append(pub)

        if len(results) == 0:
            print(f"No results found using google scholar for the current year ({current_year})" + Style.RESET_ALL)
            return f"No results found using google scholar for the current year ({current_year})"

        most_recent_result = results[0]
        # Format the results
        result = {
            "title": most_recent_result.get('bib', {}).get('title', ''),
            "authors": most_recent_result.get('bib', {}).get('author', []),
            "year": most_recent_result.get('bib', {}).get('pub_year', ''),
            "abstract": most_recent_result.get('bib', {}).get('abstract', ''),
            "url": most_recent_result.get('pub_url', '')
        }
        
        print(f"I have found the most recent result: {result['title']}")

        # Format the results
        formatted_results = []
        formatted_result = f"Title: {result['title']}\n"
        formatted_result += f"Authors: {', '.join(result['authors'])}\n"
        formatted_result += f"Year: {result['year']}\n"
        formatted_result += f"Abstract: {result['abstract']}\n"
        formatted_result += f"URL: {result['url']}\n"
        formatted_results.append(formatted_result)
        
        formatted_results = "\n".join(formatted_results)

        # Store the results in memory
        store_in_memory(formatted_results)

        print(Style.RESET_ALL)

        return formatted_results
        
    except Exception as e:
        return f"Error searching Google Scholar: {str(e)}"
    

if __name__ == "__main__":
    print(wikipedia_search("AI"))