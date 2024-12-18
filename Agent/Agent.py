from pydantic import BaseModel
from langchain_core.tools import BaseTool
from typing import Callable,Union
from graph.state import AgentState
from llm.llm_caller import LLMCaller
from config.preprint import Colors
from typing import Dict
from langchain_core.tools import StructuredTool
from langchain_core.messages import AIMessage
from pydantic import ConfigDict
class AgentFactory:
    _instance = None
    _agents: Dict[str, 'Agent'] = {}
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentFactory, cls).__new__(cls)
        return cls._instance

    def register(self, agent: 'Agent'):
        self._agents[agent.name] = agent
        
    def register_all(self,agents:list['Agent']):
        for agent in agents:
            self._agents[agent.name] = agent
            
    def get_all_agents(self) -> Dict[str, 'Agent']:
        return self._agents
    def get_agent(self,name:str):
        return self._agents.get(name)
    def initialize_all(self):
        if not self._initialized:
            for agent in self._agents.values():
                agent._get_next_agent_tools()
            self._initialized = True
            
class Agent(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str = "Agent"  # 命名规范：kodo_agent,cdn_agent,uploadfile_agent....
    model: str = "gpt-4o-mini"
    tools: list[Union[BaseTool,Callable]] = []
    tool_map: dict = {}
    instruction: str = "You are a helpful agent."   #请详细描述你的 agent 的职责功能，能做什么事
    sop: str = "对用户的提问进行回答"   #agent的规范处理任务的流程
    next_agents: list[str] = [] # 可能的下一个 agent 的名称   
    llm_caller: LLMCaller = None
    is_initialized: bool = True     # 是否初始化过，是就加上 system prompt避免冗余
    
    def __init__(self, **data):
        super().__init__(**data)
        AgentFactory().register(self)  # 注册到 AgentRegistry

    def _get_next_agent_tools(self):
        agent_factory = AgentFactory()
        all_agents = agent_factory.get_all_agents()
        next_agent_tools = []
        
        def create_transfer_func(agent):
            def transfer_func():
                return agent
            return transfer_func
        
        for next_agent in self.next_agents: #是字符串
            next_agent = all_agents.get(next_agent)  #提取出真正的agent实例
            next_agent_name = next_agent.name
            
            # 构造转移函数 tool
            tool_name = f"transfer_to_{next_agent_name}"
            tool_doc = f"将用户的问题转移到处理 {next_agent_name} 问题的 agent,该 agent 的能力是：{next_agent.instruction}"
            transfer_func = create_transfer_func(next_agent)
            transfer_func = StructuredTool.from_function(transfer_func,name=tool_name,description=tool_doc)
            next_agent_tools.append(transfer_func)
        print(f"{Colors.RED}next_agent_tools: {next_agent_tools}{Colors.ENDC}")
        self.tools = self.tools + next_agent_tools
        self.tool_map = {tool.name: tool for tool in self.tools}
        self.llm_caller = LLMCaller(model=self.model,tools=self.tools)
        
    def invoke(self,state:AgentState):
        #需要用户输入问题的情况是：已经结束单轮对话 -> ai 的回答，或者没有历史消息       
        question = state["question"]
        query = [{"role": "user", "content": "用户的问题是：" + question}]
        if self.is_initialized:     #笨蛋写法
            self.is_initialized = False
            query = [{"role": "system", "content": self.instruction + self.sop}] + query
        history = state["messages"]
        messages = history + query
        
        ai_msg = self.llm_caller.invoke(messages=messages,tool_call=True,parallel_tool_calls=False)
        
        # agent 的返回有三情况：
        # 1. 调用了tool，但是是 agent 的，转移到了下一个 agent
        # 2. 调用了内部的 tool，继续在当前 agent 处理
        # 3. 不调用tool，直接返回大模型的回答，结束单轮对话

        next_agent = self.name  #默认不转移
        if hasattr(ai_msg, "tool_calls") and len(ai_msg.tool_calls) > 0:
            # 如果 ai_msg 有 tool_calls， 调用 function拿到返回值
            tool_call =  ai_msg.tool_calls[0]   #目前只选第一个 tool call（对于 agent 的情况是这样的）
            func_name = tool_call["name"]
            args = tool_call["args"]
            print(f"Selected tool: {func_name}")
            tool_response = self.tool_map[func_name].invoke(args)
            # 如果返回的类型是 agent
            if isinstance(tool_response, Agent):
                next_agent = tool_response.name
            else:   #返回tool的结果，并结合 tool 的输入再回答一遍
                tool_message = {
                    "tool_call_id": tool_call["id"],
                    "role": "tool",
                    "name": func_name,
                    "content": tool_response
                }
                messages = messages + [ai_msg,tool_message]    #保持openai 的 Message 格式（tool 的返回值需要在 ai 的返回值后）
                ai_tool_msg = self.llm_caller.invoke(messages=messages,tool_call=True,parallel_tool_calls=False)
                messages = messages + [ai_tool_msg]
                
        else:   #不调用tool，直接返回大模型的回答，结束单轮对话，记录当前 working 的 agent，标志结束 flag
            print(f"{Colors.BOLD}ai_msg: {ai_msg.content}{Colors.ENDC}")
            messages = messages + [ai_msg]
            
        return {'question': question,'messages': messages,'next_agent': next_agent}

    async def astream(self, state:AgentState):
        question = state["question"]
        query = [{"role": "user", "content": "用户的问题是：" + question}]
        if self.is_initialized:
            self.is_initialized = False
            query = [{"role": "system", "content": self.instruction + self.sop}] + query
        history = state["messages"]
        messages = history + query
        
        # 收集完整的 AI 消息
        ai_msg = None
        first = True
        
        # 流式调用 LLM 并实时产出 token
        async for chunk in self.llm_caller.astream(messages=messages,tool_call=True):
            if first:
                ai_msg = chunk
                first = False
            else:
                ai_msg = ai_msg + chunk
            yield chunk

        # 处理工具调用
        next_agent = self.name  # 默认不转移
        if hasattr(ai_msg, "tool_calls") and len(ai_msg.tool_calls) > 0:
            tool_call = ai_msg.tool_calls[0]
            func_name = tool_call["name"]
            args = tool_call["args"]
            print(f"Selected tool: {func_name}")
            tool_response = self.tool_map[func_name].invoke(args)
            
            if isinstance(tool_response, Agent):
                next_agent = tool_response.name
            else:
                tool_message = {
                    "tool_call_id": tool_call["id"],
                    "role": "tool", 
                    "name": func_name,
                    "content": tool_response
                }
                messages = messages + [ai_msg,tool_message]
                
                # 再次流式调用 LLM
                async for chunk in self.llm_caller.astream(messages=messages,tool_call=True):
                    yield chunk
                
        else:
            print(f"{Colors.BOLD}ai_msg: {ai_msg.content}{Colors.ENDC}")
            messages = messages + [ai_msg]
            
        yield {'question': question,'messages': messages,'next_agent': next_agent}
