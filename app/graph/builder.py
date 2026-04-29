from langgraph.graph import StateGraph, START, END
from app.graph.state import AgentState

from app.agents.planner import planner_agent
from app.agents.developer import developer_agent
from app.agents.tester import tester_agent
from app.agents.reviewer import reviewer_agent

def should_retry(state):
    if state["test_passed"]:
        return "pass"
    elif state.get("iterations", 0) > 3:
        return "pass" 
    else:
        return "retry"

def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("planner", planner_agent)
    builder.add_node("developer", developer_agent)
    builder.add_node("tester", tester_agent)
    builder.add_node("reviewer", reviewer_agent)

    builder.add_edge(START, "planner")
    builder.add_edge("planner", "developer")
    builder.add_edge("developer", "tester")
    builder.add_conditional_edges(
        "tester",
        should_retry,
        {
            "retry": "developer",
            "pass": "reviewer"
        }
    )
    builder.add_edge("reviewer", END)

    return builder.compile()