import logging
import json
import os
from datetime import datetime
from typing import Any

class Engine:
    def __init__(self, session_file="state/session.json"):
        self.session_file = session_file
        # Automatically create necessary folders so you don't have to
        self.ensure_directories()
        self.setup_logging()
        
    def ensure_directories(self):
        os.makedirs("logs", exist_ok=True)
        os.makedirs("state", exist_ok=True)
        os.makedirs("data", exist_ok=True)

    def setup_logging(self):
        # Creates a unique log file for every run based on the time
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"logs/run_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            # Format: Time - Level - Agent Name - Message
            format='%(asctime)s - [%(levelname)s] - [%(name)s] - %(message)s',
            handlers=[
                logging.FileHandler(log_file), # Save to file
                logging.StreamHandler()        # Print to screen
            ]
        )
        self.logger = logging.getLogger("DataSteward")
        self.logger.info(f"Engine Initialized. Logging to {log_file}")

    def log(self, agent: str, action: str, details: str):
        """Records an event to the log file."""
        self.logger.info(f"[{agent}] {action}: {details}")

    def save_state(self, key: str, value: Any):
        """Persistent Memory: Saves key-value pairs to session.json"""
        data = {}
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {} # Reset if corrupt
        
        data[key] = value
        
        with open(self.session_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)