import subprocess
import uuid
import os
import shutil
import re

def clean_code(code: str):
    if "```" in code:
        parts = code.split("```")
        code = parts[1]
        if code.startswith("java"):
            code = code[4:]
    return code.strip()


def run_java_in_docker(code: str):
    temp_dir = None

    try:
        # clean code
        code = clean_code(code)

        # prevent input-based programs
        if "Scanner" in code or "System.in" in code:
            return {
                "success": False,
                "error": "Input-based programs are not allowed"
            }
        
        # create unique temp directory
        container_id = f"java_exec_{uuid.uuid4().hex[:6]}"
        temp_dir = f"temp_{container_id}"
        os.mkdir(temp_dir)

        # ensure class name = main
        code = re.sub(r'class\s+\w+', 'class Main', code)

        java_file = os.path.join(temp_dir, "Main.java")

        with open(java_file, "w") as f:
            f.write(code)

        path = os.path.abspath(temp_dir).replace("\\", "/")

        # run inside docker
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                "-v", f"{path}:/app",
                "eclipse-temurin:17-jdk",
                "bash", "-c",
                "javac /app/Main.java && java -cp /app Main"
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return {
                "success": False,
                "error": result.stderr
            }
        
        return {
            "success": True,
            "output": result.stdout.strip()
        }
    
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Execution timed out"
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    
    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)