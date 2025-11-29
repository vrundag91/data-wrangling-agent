import os
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm():
    """
    Connects to Google Gemini 2.5 Flash.
    Assumes GOOGLE_API_KEY is already set in environment by main.py
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("API Key is missing! Make sure main.py sets it.")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0.0,
        google_api_key=api_key
    )
    
    return llm