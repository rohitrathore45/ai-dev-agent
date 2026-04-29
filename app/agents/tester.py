from app.tools.docker_executor import run_java_in_docker

def tester_agent(state):
    code = state["code"]

    result = run_java_in_docker(code)

    if result["success"]:
        return {
            "messages": state["messages"] + ["PASS"],
            "feedback": result.get("output", "Execution successful"),
            "test_passed": True
        }
    else:
        return {
            "messages": state["messages"] + [result["error"]],
            "feedback": result["error"],
            "test_passed": False
        }