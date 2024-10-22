from typing import Dict, Any, List, Callable
from langchain_core.tools import BaseTool, tool

class ToolRegistry:
    _tools: Dict[str, Callable] = {}

    @classmethod
    def register(cls, func: Callable):
        cls._tools[func.name] = func
        print("register tool:",func.name)
        return func

    @classmethod
    def get_tool(cls, tool_name: str) -> Callable:
        return cls._tools.get(tool_name)

    @classmethod
    def get_langchain_tools(cls) -> List[BaseTool]:
        return [func for func in cls._tools.values()]

    @classmethod
    def get_tool_info(cls, tool_name: str) -> Dict[str, Any]:
        tool_func = cls.get_tool(tool_name)
        if tool_func is None:
            raise ValueError(f"Tool '{tool_name}' not found in registry")
        tool_schema = tool_func.args_schema.schema()
        tool_description = tool_schema['description']
        tool_args_schema = tool_schema['properties']
        
        
        tool_info = {
            "tool_name": tool_name,
            "tool_description": tool_description,
            "tool_args_schema": str(tool_args_schema),
        }
        tool_info_str = "the tool name is \"{tool_name}\", the tool description is \"{tool_description}\", \
                        the tool input args schema is \"{tool_args_schema}\"".format(**tool_info)
        return tool_info_str        

    @classmethod
    def get_all_tools_info(cls) -> List[Dict[str, Any]]:
        return [cls.get_tool_info(name) for name in cls._tools]