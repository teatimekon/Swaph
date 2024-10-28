from typing import Callable,Union

from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from time import time
from config.preprint import Colors
class LLMCaller:
    def __init__(self,model="gpt-4o-mini",tools:list[Union[BaseTool,Callable]]=[]):
        self.llm = ChatOpenAI(model=model, api_key="sk-WbEpTniVLtZbePrk3e4fE2B1AbCd43B6B0FcCaC5A0478934", base_url="https://api2.aigcbest.top/v1")
        self.llm_with_tool = self.llm
        self.tools = tools
        if self.tools:
            self.llm_with_tool = self.llm_with_tool.bind_tools(self.tools)
        
    def invoke(self, messages,tool_call=False, **kwargs):
        llm_to_use = self.llm_with_tool if tool_call else self.llm
        start_time = time()
        if  "parallel_tool_calls" in kwargs:
            llm_to_use = llm_to_use.bind_tools(self.tools,**kwargs)
        
        ai_msg = llm_to_use.invoke(messages, **kwargs)
        end_time = time()
        execution_time = end_time - start_time
        print(f"{Colors.OKGREEN}LLM 执行时间: {execution_time:.2f}秒{Colors.ENDC}")
        return ai_msg
    async def astream(self, messages, tool_call=False, **kwargs):
        llm_to_use = self.llm_with_tool if tool_call else self.llm
        if "parallel_tool_calls" in kwargs:
            llm_to_use = llm_to_use.bind_tools(self.tools,**kwargs)
            
        stream = await llm_to_use.astream(messages, **kwargs)
        async for chunk in stream:
            yield chunk
            
    def bind_tools(self, tools:list[BaseTool]):
        self.tools.append(tools)
        self.llm_with_tool = self.llm.bind_tools(tools)
