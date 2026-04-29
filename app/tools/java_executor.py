import subprocess
import os
import uuid
import re

def clean_code(code:str):
    if "```" in code:
        code = code.split("```")[1]
        if code.startswith("java"):
            code = code[4:]
    return code.strip()

def run_java_code(code: str):

    classname = None
    filename = None

    try:
        code = clean_code(code)

        classname = f"Main{uuid.uuid4().hex[:6]}"
        filename = f"{classname}.java"

        code = re.sub(r'class\s+Main', f'class {classname}', code)

        # create temp file
        with open(filename, "w") as f:
            f.write(code)

        # compile
        compile_process = subprocess.run(
            ["javac", filename],
            capture_output=True,
            text=True,
            timeout=5
        )

        if compile_process.returncode != 0:
            return {
                "success": False,
                "error": compile_process.stderr
            }
        
        # run
        run_process = subprocess.run(
            ["java", classname],
            input="",
            capture_output=True,
            text=True,
            timeout=5
        )

        if run_process.returncode != 0:
            return { "success": False, "error": run_process.stderr}

        output = run_process.stdout

        return {"success": True, "output": output}
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    
    finally:
        try:
            if filename and os.path.exists(filename):
                os.remove(filename)
            if classname and os.path.exists(f"{classname}.class"):
                os.remove(f"{classname}.class")
        except:
            pass