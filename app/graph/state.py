from typing import TypedDict, List

class AgentState(TypedDict):
    messages: List[str]
    task: str
    code: str
    feedback: str