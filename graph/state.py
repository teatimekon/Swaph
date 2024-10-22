from typing import Annotated
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

class AgentState(TypedDict):
    question: str
    messages: Annotated[list, add_messages]
    next_agent: str
