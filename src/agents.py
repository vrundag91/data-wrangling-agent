from langchain_core.messages import HumanMessage, SystemMessage
from src.llm import get_llm
from src.tools import execute_python_code

class BaseAgent:
    def __init__(self, name, engine):
        self.name = name
        self.engine = engine
        self.llm = get_llm()

    def log(self, action, details):
        self.engine.log(self.name, action, details)

class AnalystAgent(BaseAgent):
    def run(self, csv_head_str):
        self.log("Start", "Analyzing CSV structure for quality issues")
        
        prompt = f"""
        You are a Senior Data Quality Analyst.
        Here are the first 5 rows of a dataset:
        
        {csv_head_str}
        
        Your Task:
        Identify 3-5 critical data quality issues (e.g., missing values, inconsistent date formats, mixed data types, typos).
        
        Output Format:
        Return ONLY a bulleted list of the issues found. Do not write code.
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        result = response.content
        
        self.log("Complete", "Analysis finished")
        return result

class CoderAgent(BaseAgent):
    def run(self, issues_list, file_path):
        self.log("Start", "Generating cleaning code based on analysis")
        
        prompt = f"""
        You are an Expert Python Data Engineer.
        
        Input File: {file_path}
        Issues to Fix:
        {issues_list}
        
        Your Task:
        Write a complete, executable Python script using the 'pandas' library to fix these issues.
        
        Constraints:
        1. Load the data from '{file_path}'.
        2. Fix the issues mentioned.
        3. Save the cleaned dataframe to 'data/cleaned_data.csv'.
        4. Print the message "Done" at the end of the script.
        5. Handle potential errors using try/except blocks.
        6. Return ONLY the python code. No explanations.
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        raw_code = response.content
        
        # Cleaning the output (Removing markdown backticks if present)
        clean_code = raw_code.replace("```python", "").replace("```", "").strip()
        
        self.log("Action", "Executing generated Python code...")
        
        # Using the Tool from tools.py
        execution_result = execute_python_code(clean_code)
        
        self.log("Result", "Code execution finished")
        return execution_result, clean_code

class ReviewerAgent(BaseAgent):
    def run(self, original_issues, execution_log, code_snippet):
        self.log("Start", "Evaluating the cleaning process")
        
        prompt = f"""
        You are a QA Lead. Evaluate the automated data cleaning job.
        
        Original Issues Detected:
        {original_issues}
        
        Code Executed:
        {code_snippet}
        
        Execution Output:
        {execution_log}
        
        Your Task:
        1. Did the code run successfully?
        2. Does the code address the original issues?
        3. Assign a Quality Score (0-100).
        
        Output Format:
        Provide a brief summary and the final score.
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        result = response.content
        
        self.log("Complete", f"Evaluation: {result}")
        return result