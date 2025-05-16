from typing import Optional, Any, Dict
from langchain.tools import BaseTool
from datetime import datetime
import os
import json
from pydantic import Field

class SaveTool(BaseTool):
    name: str = "save_to_file"
    description: str = "Save the query results to a text file. Input should be a JSON string containing the results."
    output_dir: str = Field(default="outputs", description="Directory where files will be saved")
    
    def __init__(self, output_dir: str = "outputs"):
        super().__init__()
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def _run(self, content: str) -> str:
        """
        Save the content to a text file with timestamp.
        
        Args:
            content (str): The content to save (should be a JSON string)
            
        Returns:
            str: Path to the saved file
        """
        try:
            # Try to parse the content as JSON
            if isinstance(content, str):
                try:
                    data = json.loads(content)
                except json.JSONDecodeError:
                    # If it's not valid JSON, save it as is
                    data = {"content": content}
            else:
                data = content

            # Format the content nicely
            formatted_content = json.dumps(data, indent=2)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"query_result_{timestamp}.txt"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(formatted_content)
            return f"Successfully saved results to {filepath}"
        except Exception as e:
            return f"Error saving results: {str(e)}"
    
    async def _arun(self, content: str) -> str:
        """Async implementation of _run"""
        return self._run(content)
