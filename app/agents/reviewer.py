from langchain_openai import ChatOpenAI
from app.services.llm import llm

def reviewer_agent(state):
    
    code = state["code"]

    messages = [
        {
        "role": "system",
        "content": """You are a senior code reviewer.

        Rules:
        - Improve code for readability and best practices
        - Return ONLY valid Java code
        - Do NOT include explanations, markdown, or extra text
        """
        },
        {"role": "user", "content": f"""
        Improve this code for:
        - readability
        - performance
        - best practices
        Code:
        {code}
        """}
    ]

    response = llm.invoke(messages)

    return {
        "messages": state["messages"] + [response.content],
        "code": response.content
    }