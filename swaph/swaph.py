from graph.state import AgentState
from Agent import Agent, AgentFactory
from config.preprint import Colors
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from graph.AgentGraph import AgentGraph
from config.prompt_class import Prompt
from typing import List, Dict, Any
from tool import ToolRegistry
from langchain_core.messages import AIMessageChunk
class Swaph:
    def __init__(self):
        self.agent_factory = AgentFactory()
        self.graph = None
        self.memory = MemorySaver()
        self.config = {"configurable": {"thread_id": "1"}}


    def create_agents(self,model="gpt-4o-mini"):
        router_agent = Agent(name="router_agent",
                             model=model,
                             next_agents=["search_agent", "kodo_agent"],
                            #  instruction="你是路由专家，能根据用户的问题，将用户的问题转移到对应的 agent",
                            instruction="你是智能助手"
                            #  sop=Prompt.get_prompt(name="router")
                             )
        kodo_agent = Agent(name="kodo_agent",
                           model=model,
                           tools=[ToolRegistry.get_tool("download_file"),ToolRegistry.get_tool("upload_file")],
                           instruction="你是kodo的专家，能处理kodo相关的问题，例如：如何上传文件到kodo，如何下载文件到kodo，如何删除文件到kodo，如何查询文件到kodo，如何添加文件到kodo")
        search_agent = Agent(name="search_agent",
                          model=model,
                          tools=[ToolRegistry.get_tool("search_tool")],
                          instruction="你是搜索引擎的专家，能处理搜索引擎相关的问题，例如：如何搜索，如何查询，如何删除，如何添加")

        self.agent_factory.register_all([router_agent, search_agent, kodo_agent])
        self.agent_factory.initialize_all()

    def initialize_graph(self):
        agent_graph = AgentGraph(self.agent_factory)
        agent_graph.set_entry_agent_node("router_agent")
        agent_graph.init_graph()
        self.graph = agent_graph.graph.compile(checkpointer=self.memory)

    def save_graph_image(self, filename: str = "graph.png"):
        graph_image = self.graph.get_graph().draw_mermaid_png()
        with open(filename, "wb") as f:
            f.write(graph_image)
        print(f"图片已保存为 {filename}")

    def invoke(self, question: str, conversation_id: str) -> Dict[str, Any]:
        config = {"configurable": {"thread_id": conversation_id}}
        ans = self.graph.invoke({"question": question}, config=config)
        
        # 打印执行时间统计
        if "execution_times" in ans:
            print("\n执行时间统计:")
            for agent_name, exec_time in ans["execution_times"].items():
                print(f"{agent_name}: {exec_time:.2f}秒")
        return ans
    
    def stream(self,question:str,conversation_id:str):
        config = {"configurable": {"thread_id": conversation_id}}
        stream_response = self.graph.stream({"question": question}, config=config, stream_mode="messages")
        for message, metadata in stream_response:
            # 只处理 AIMessageChunk 类型的消息
            if isinstance(message, AIMessageChunk):
                # 你可以在这里添加任何需要的处理逻辑
                processed_content = message.content
                # 使用 yield 返回处理后的内容
                yield processed_content
                
                
    async def astream(self, question:str, conversation_id:str):
        config = {"configurable": {"thread_id": conversation_id}}
        stream_response = self.graph.astream(
            {"question": question}, 
            config=config,
            stream_mode="messages"
        )
        async for message, metadata in stream_response:
            print(message)
            if isinstance(message, AIMessageChunk):
            
                yield message.content
                
    def pretty_print_messages(self, messages: List[Any]):
        for message in messages:
            message.pretty_print()

    def setup(self,model="gpt-4o-mini"):
        self.create_agents(model)
        self.initialize_graph()
        self.save_graph_image()

    def run(self):
        self.setup()
        while True:
            question = input("请输入问题（输入'退出'结束）: ")
            if question.lower() == '退出':
                break
            ans = self.invoke(question, "1")
            self.pretty_print_messages(ans["messages"])
            print("next_agent: ", ans["next_agent"])

# 使用示例
# if __name__ == "__main__":
#     swaph = Swaph()
#     swaph.run()

