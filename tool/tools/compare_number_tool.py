#比较两个数字大小 tool
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool, tool
from tool import ToolRegistry

class CompareNumberToolInput(BaseModel):
    """
    比较两个数字大小，输入是两个数字，输出是两个数字的大小关系
    """
    num1: float = Field(description="第一个数字")
    num2: float = Field(description="第二个数字")

@ToolRegistry.register
@tool("compare_number_tool", args_schema=CompareNumberToolInput)
def compare_number_tool(num1: float, num2: float) -> str:
    if num1 > num2:
        return f"{num1} 大于 {num2}"
    elif num1 < num2:
        return f"{num1} 小于 {num2}"
    else:
        return f"{num1} 等于 {num2}"
