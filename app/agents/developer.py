from langchain_openai import ChatOpenAI
from app.services.llm import llm

def developer_agent(state):

    task = state["task"]
    plan = state["plan"]
    feedback = state.get("feedback", "")
    current_code = state.get("code", "")

    messages = [
        {
            "role": "system",
            "content": """You are a senior software engineer.

            Rules:
            - Use ONLY plain Java (single file, Main class)
            - DO NOT use Scanner, BufferedReader, or any input methods
            - Use hardcoded values or sample values
            - Code must run without user input
            """
        },
        {
            "role": "user",
            "content": f"""
            Task:
            {task}

            Plan:
            {plan}

            Existing code:
            {current_code}

            Feedback:
            {feedback}

            If there are compilation or runtime errors, FIX them.
            Return ONLY valid Java code
            """
        }
    ]

    response = llm.invoke(messages)

    return {
        "messages": state["messages"] + [response.content],
        "code": response.content,
        "iterations": state.get("iterations", 0) + 1
    }