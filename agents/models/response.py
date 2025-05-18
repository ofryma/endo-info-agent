from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

class Source(BaseModel):
    title: str = Field(..., description="The title of the source")
    url: str = Field(..., description="The url of the source")

class AgentResult(BaseModel):

    """Model for agent results."""
    title: str = Field(..., description="The title of the result")
    short_description: str = Field(..., description="A short description of the result")
    description: str = Field(..., description="A detailed description of the result with all relevant information")
    tools_used: List[str] = Field(..., description="The tools used to get the result")

    @field_validator('tools_used')
    @classmethod
    def lowercase_tools(cls, v: List[str]) -> List[str]:
        return [tool.lower() for tool in v]

class AgentResponse(BaseModel):

    query: str = Field(..., description="The query to search for")
    output: str = Field(..., description="The output of the query")

class CalenderEvent(BaseModel):
    title: str = Field(..., description="The title of the event")
    description: str = Field(..., description="The description of the event")
    start_date: str = Field(..., description="The start date of the event")
    end_date: str = Field(..., description="The end date of the event")
    location: str = Field(..., description="The location of the event")
