import subprocess
import sys
import os

def execute_python_code(code_str: str, cwd: str = ".") -> str:
    """
    Executes a Python script string in a separate process.
    Captures stdout (print output) and stderr (errors).
    """
    # 1. Define the temporary filename
    filename = "temp_agent_script.py"
    filepath = os.path.join(cwd, filename)
    
    # 2. Write the code string to that file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code_str)
    
    # 3. Run the script using the current python interpreter
    try:
        result = subprocess.run(
            [sys.executable, filename], # Uses the same python as your venv
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30 # Fails if code takes longer than 30s
        )
        
        # 4. Return the results
        if result.returncode == 0:
            return f"SUCCESS:\n{result.stdout}"
        else:
            return f"ERROR:\n{result.stderr}"

    except Exception as e:
        return f"EXECUTION FAILED: {str(e)}"