from langchain_openai import ChatOpenAI
from app.config import OPENAI_API_KEY


def planner_agent(state):
    llm = ChatOpenAI(model = "gpt-4o-mini", api_key=OPENAI_API_KEY)

    task = state["task"]
    
    messages = [
        {"role": "system", "content": "You are a software project planner."},
        {"role": "user", "content": f"Break this task into clear development steps:\n{task}"}
    ]

    response = llm.invoke(messages)

    return {
        "messages": state["messages"] + [response.content]
    }