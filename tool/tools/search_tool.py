from tool import ToolRegistry  # 修改这里
from langchain_core.tools import BaseTool,tool
from langchain_community.tools import DuckDuckGoSearchRun
from typing import Dict, Any, Type,Annotated
from pydantic import BaseModel, Field
class SearchToolInput(BaseModel):
    """
    Useful for searching the internet
    """
    query: str = Field(description="The query to search for")

@ToolRegistry.register
@tool("search_tool",args_schema=SearchToolInput)
def search_tool(query: str) -> str:
    
    search_tool = DuckDuckGoSearchRun()
    return search_tool.invoke(query)   