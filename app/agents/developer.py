from langchain_openai import ChatOpenAI
from app.config import OPENAI_API_KEY

def developer_agent(state):
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

    plan = state["messages"][-1]

    messages = [
        {"role": "system", "content": "You are a senior software engineer."},
        {"role": "user", "content": f"Write working code based on this plan:\n{plan}"}
    ]

    response = llm.invoke(messages)

    return {
        "messages": state["messages"] + [response.content],
        "code": response.content
    }