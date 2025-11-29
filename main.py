import pandas as pd
import os
import glob
import getpass
import json
import re
from datetime import datetime
from src.engine import Engine
from src.agents import AnalystAgent, CoderAgent, ReviewerAgent

def setup_api_key():
    if not os.getenv("GOOGLE_API_KEY"):
        print("🔑 Authentication Required")
        print("Please paste your Google Gemini API Key below:")
        key = getpass.getpass("API Key: ")
        os.environ["GOOGLE_API_KEY"] = key.strip()

def extract_score(text):
    """Helper to extract a number (0-100) from the Reviewer's text."""
    match = re.search(r'\b(100|[1-9]?[0-9])\b', text)
    return int(match.group(0)) if match else 0

def main():
    setup_api_key()
    engine = Engine()
    
    input_dir = "data/raw"
    output_dir = "data/clean"
    report_file = "processing_report.json"  # <--- NEW: The Flight Recorder
    
    os.makedirs(output_dir, exist_ok=True)
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))
    
    # This list will hold the summary of every run
    session_report = [] 

    print(f"--- Found {len(csv_files)} files to process ---")

    for i, file_path in enumerate(csv_files):
        file_name = os.path.basename(file_path)
        print(f"\n[Batch {i+1}/{len(csv_files)}] Processing: {file_name}")
        
        # Initialize record for this file
        record = {
            "filename": file_name,
            "timestamp": datetime.now().isoformat(),
            "status": "Failed", # Default
            "issues_detected": "",
            "quality_score": 0,
            "reviewer_comments": ""
        }

        try:
            safe_input_path = file_path.replace("\\", "/")
            safe_output_path = os.path.join(output_dir, f"clean_{file_name}").replace("\\", "/")

            df = pd.read_csv(file_path)
            csv_head = df.head().to_string()
            
            # 1. Analyst
            print("  > Analyst is thinking...")
            analyst = AnalystAgent("Analyst", engine)
            issues = analyst.run(csv_head)
            record["issues_detected"] = issues  # <--- Capture output

            # 2. Coder
            print("  > Coder is fixing...")
            coder = CoderAgent("Coder", engine)
            instruction = (
                f"Load '{safe_input_path}'. Fix issues. "
                f"Save strictly to '{safe_output_path}'. Use index=False."
            )
            exec_result, code = coder.run(issues, instruction)
            
            # 3. Reviewer
            print("  > Reviewer is grading...")
            reviewer = ReviewerAgent("Reviewer", engine)
            grade = reviewer.run(issues, exec_result, code)
            
            # Save Reviewer Details
            record["reviewer_comments"] = grade
            record["quality_score"] = extract_score(grade) # Extract number for charts
            record["status"] = "Success"

            print(f"  ✅ Done! Score: {record['quality_score']}/100")
            
        except Exception as e:
            print(f"  ! FAILED: {e}")
            record["status"] = f"Error: {str(e)}"
        
        # Add to session report
        session_report.append(record)

    # Save the full report to JSON
    with open(report_file, "w") as f:
        json.dump(session_report, f, indent=2)
    
    print(f"\n--- Batch Complete. Report saved to {report_file} ---")

if __name__ == "__main__":
    main()