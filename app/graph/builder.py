from langgraph.graph import StateGraph, START, END
from app.graph.state import AgentState
from app.agents.planner import planner_agent
from app.agents.developer import developer_agent

def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("planner", planner_agent)
    builder.add_node("developer", developer_agent)

    builder.add_edge(START, "planner")
    builder.add_edge("planner", "developer")
    builder.add_edge("developer", END)

    return builder.compile()