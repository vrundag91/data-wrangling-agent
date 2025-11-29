from pydantic import BaseModel, Field
from typing import Optional, List, Any

# This mimics the "Task" and "Artifact" structure of A2A protocols
# It ensures every agent returns data in exactly this shape.

class AgentOutput(BaseModel):
    agent_name: str
    status: str = Field(description="success or failure")
    summary: str = Field(description="A brief summary of what the agent did")
    data: Any = Field(description="The actual payload (e.g., list of issues, code string, or score)")
    artifacts: List[str] = Field(default=[], description="List of files created or modified (e.g., ['cleaned_data.csv'])")