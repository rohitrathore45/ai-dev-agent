from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.graph.builder import build_graph
from pydantic import BaseModel

app = FastAPI()
graph = build_graph()

class TaskRequest(BaseModel):
    task: str

@app.get("/")
def home():
    return {
        "message": "AI DEV Agent Running"
    }

@app.post("/run")
async def run_agent(request: TaskRequest):
    state = {
        "messages": [],
        "task": request.task,
        "code": "",
        "feedback": ""
    }

    result = graph.invoke(state)

    return {
        "task": request.task,
        "output": result["messages"],
        "code": result.get("code", "")
    }