from pydantic import BaseModel, Field      # 定义传入的参数模式，打上准确的描述标签
from langchain_core.tools import BaseTool, tool
from tool import ToolRegistry 

from typing import Type, Optional, Dict, Any, Annotated
from datetime import datetime
import pytz

#根据传入的时区，返回当前时间
class GetTimeToolInput(BaseModel):
    "useful when you need to know the current/today/now time, this tool can get the current/today/now time"
    timezone: str = Field(description="The timezone mentioned in the query,like 'Asia/Shanghai',if you don't know the timezone,or the timezone is not mentioned,just use default timezone 'Asia/Shanghai'")

@ToolRegistry.register
@tool("get_time_tool",args_schema=GetTimeToolInput)
def get_time_tool(timezone:str) -> str:
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
        return f"当前时间是 {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    except pytz.exceptions.UnknownTimeZoneError:
        return f"无效的时区: {timezone}。请使用有效的时区，例如 'Asia/Shanghai'。"
