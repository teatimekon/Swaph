from graph.state import AgentState
from Agent import Agent,AgentFactory
from config.preprint import Colors
from langchain_core.tools import tool
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import MemorySaver
from graph.AgentGraph import AgentGraph
import asyncio
@tool
def handle_kodo_question():
    """ 
    处理kodo相关的问题
    """
    print(f"{Colors.OKBLUE}handle_kodo_question{Colors.ENDC}")
    return "处理完成！"

@tool
def handle_cdn_question(question:str):
    """ 
    处理cdn相关的问题
    """
    print(f"{Colors.OKBLUE}handle_cdn_question{Colors.ENDC}",question)
    return "处理完成！"

from config.prompt_class import Prompt
router_agent = Agent(name="router_agent",
                    model="gpt-4o-mini",
                    next_agents=["cdn_agent","kodo_agent"],
                    instruction="你是路由专家，能根据用户的问题，将用户的问题转移到对应的 agent",
                    sop=Prompt.get_prompt(name="router"))
kodo_agent = Agent(name="kodo_agent",
                   model="gpt-4o-mini",
                   tools=[handle_kodo_question],
                   instruction="你是kodo的专家，能处理kodo相关的问题，例如：如何上传文件到kodo，如何下载文件到kodo，如何删除文件到kodo，如何查询文件到kodo")
cdn_agent = Agent(name="cdn_agent",
                  model="gpt-4o-mini",
                  tools=[handle_cdn_question],
                  instruction="你是cdn的专家，能处理cdn相关的问题，例如：如何配置cdn，如何查询cdn，如何删除cdn，如何添加cdn")

AgentFactory().register_all([router_agent,cdn_agent,kodo_agent])
AgentFactory().initialize_all()

graph = AgentGraph(AgentFactory())
graph.set_entry_agent_node("router_agent")
graph.init_graph()
graph = graph.graph

memory = MemorySaver()

graph = graph.compile(checkpointer=memory)

graph_image = graph.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(graph_image)
print("图片已保存为 graph.png")

config = {"configurable": {"thread_id": "1"}}



from langchain_core.messages import SystemMessage,HumanMessage,AIMessageChunk
while True:
    question = input("请输入问题：")
    for msg,metadata in graph.stream({"question": question}, config=config, stream_mode="messages"):
        if isinstance(msg,AIMessageChunk):
            print(msg.content,end="｜",flush=True)


    
        
