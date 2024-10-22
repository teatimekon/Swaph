tool定义：
tool 定义成为函数，参考get_time_tool.py和search_tool.py

tool注册：
使用ToolRegistry.register装饰器进行注册，参考get_time_tool.py，之后在 init 文件中导入即可

tool调用：
使用ToolRegistry.get_tool_info获取tool信息，也能获取函数等