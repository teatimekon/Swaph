from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool, tool
from tool import ToolRegistry

class CalculatorToolInput(BaseModel):
    """
    只能进行加减乘除四种运算，输入是两个数字和一个运算符，输出是计算结果
    """
    num1: float = Field(description="第一个数字")
    num2: float = Field(description="第二个数字")
    operator: str = Field(description="运算符 (+, -, *, /)")

@ToolRegistry.register
@tool("calculator_tool", args_schema=CalculatorToolInput)
def calculator_tool(num1: float, num2: float, operator: str) -> str:
    try:
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                return "错误: 除数不能为零"
            result = num1 / num2
        else:
            return f"错误: 不支持的运算符 '{operator}'"
        
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算出错: {str(e)}"