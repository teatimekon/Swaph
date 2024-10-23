from graph.state import AgentState
from Agent import Agent, AgentFactory
from config.preprint import Colors
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from graph.AgentGraph import AgentGraph
from config.prompt_class import Prompt
from typing import List, Dict, Any

class Swaph:
    def __init__(self):
        self.agent_factory = AgentFactory()
        self.graph = None
        self.memory = MemorySaver()
        self.config = {"configurable": {"thread_id": "1"}}

    @tool
    def handle_kodo_question(self):
        """ 
        处理kodo相关的问题
        """
        print(f"{Colors.OKBLUE}handle_kodo_question{Colors.ENDC}")
        return "处理完成！"

    @tool
    def handle_cdn_question(self, question: str):
        """ 
        处理cdn相关的问题
        """
        print(f"{Colors.OKBLUE}handle_cdn_question{Colors.ENDC}", question)
        return "处理完成！"

    def create_agents(self):
        router_agent = Agent(name="router_agent",
                             model="gpt-4o-mini",
                             next_agents=["cdn_agent", "kodo_agent"],
                             instruction="你是路由专家，能根据用户的问题，将用户的问题转移到对应的 agent",
                             sop=Prompt.get_prompt(name="router"))
        kodo_agent = Agent(name="kodo_agent",
                           model="gpt-4o-mini",
                           tools=[self.handle_kodo_question],
                           instruction="你是kodo的专家，能处理kodo相关的问题，例如：如何上传文件到kodo，如何下载文件到kodo，如何删除文件到kodo，如何查询文件到kodo")
        cdn_agent = Agent(name="cdn_agent",
                          model="gpt-4o-mini",
                          tools=[self.handle_cdn_question],
                          instruction="你是cdn的专家，能处理cdn相关的问题，例如：如何配置cdn，如何查询cdn，如何删除cdn，如何添加cdn")

        self.agent_factory.register_all([router_agent, cdn_agent, kodo_agent])
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

    def invoke(self, question: str) -> Dict[str, Any]:
        ans = self.graph.invoke({"question": question}, config=self.config)
        return ans

    def pretty_print_messages(self, messages: List[Any]):
        for message in messages:
            message.pretty_print()

    def setup(self):
        self.create_agents()
        self.initialize_graph()
        self.save_graph_image()

    def run(self):
        self.setup()
        while True:
            question = input("请输入问题（输入'退出'结束）: ")
            if question.lower() == '退出':
                break
            ans = self.invoke(question)
            self.pretty_print_messages(ans["messages"])
            print("next_agent: ", ans["next_agent"])

# 使用示例
if __name__ == "__main__":
    swaph = Swaph()
    swaph.run()

