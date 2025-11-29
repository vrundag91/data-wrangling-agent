# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (git is often needed for some python packages)
RUN apt-get update && apt-get install -y git

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Default command: Setup data then run the agent
CMD ["sh", "-c", "python setup_data.py && python main.py"]