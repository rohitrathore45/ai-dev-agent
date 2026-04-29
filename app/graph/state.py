from typing import TypedDict, List

class AgentState(TypedDict):
    messages: List[str]
    task: str
    plan: str
    code: str
    feedback: str
    test_passed: bool
    iterations: int