from Agent import AgentFactory
from graph.state import AgentState
from langgraph.graph import StateGraph
from config.preprint import Colors
from langgraph.graph import START

class AgentGraph:
    def __init__(self,agent_factory:AgentFactory):
        self.graph = StateGraph(AgentState)
        self.agent_factory = agent_factory
        self.entry_agent_node = None

        
    # 添加所有 agent 节点
    def add_all_agent_node(self):
        for agent in self.agent_factory.get_all_agents().values():
            print(f"{Colors.GREY}add agent node: {agent.name}{Colors.ENDC}")
            self.graph.add_node(agent.name, agent.invoke)
    
    # 设置入口节点
    def set_entry_agent_node(self,entry_node:str):
        self.entry_agent_node = entry_node

    # 路由到下一个 agent
    def route_to_agent(self,state):
        if "next_agent" not in state: 
            #刚开始没有消息，默认返回 entry_agent_node
            return self.entry_agent_node
        #有消息，判断消息的最后一条是不是 ai message，是则返回 END，否则返回 next_agent
        # last_message = state["messages"][-1]
        # if isinstance(last_message,AIMessage):
        #     return END
        print("route to agent: ",state["next_agent"])
        return state["next_agent"]
    # 添加条件边
    # Agent有三条边：
    # 1. 路由到自己
    # 2. 路由到下一个 agent
    # 3. 路由到入口节点
    def add_conditional_edges(self):
        self.graph.add_conditional_edges(
            START,
            self.route_to_agent,
        )
        for agent in self.agent_factory.get_all_agents().values():
            self.graph.add_conditional_edges(
                agent.name,
                self.route_to_agent,
            )
    def init_graph(self):
        self.add_all_agent_node()
        self.add_conditional_edges()
        
        