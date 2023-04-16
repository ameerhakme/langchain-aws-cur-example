# Use the official Python base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy your Python files and requirements.txt into the container
COPY app.py main.py agent.py config.py requirements.txt /app/

# Install any necessary dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run the FastAPI app using Uvicorn when the container launches
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
