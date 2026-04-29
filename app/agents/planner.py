from app.services.llm import llm

def planner_agent(state):
    task = state["task"]

    messages = [
        {
            "role": "system",
            "content": """You are a software project planner for an autonomous coding agent.

Rules:
- The code will run in a NON-INTERACTIVE environment.
- DO NOT include user input methods (Scanner, System.in, BufferedReader).
- The solution MUST be a single-file Java program.
- The main class MUST be named 'Main'.
- The program must compile with: javac Main.java
- The program must run with: java Main
- Keep the solution simple and executable.
"""
        },
        {
            "role": "user",
            "content": f"""
Break this task into clear development steps for implementation:

Task:
{task}
"""
        }
    ]

    response = llm.invoke(messages)

    return {
        "messages": state["messages"] + [response.content],
        "plan": response.content
    }