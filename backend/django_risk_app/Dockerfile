# Use official Python image as base
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Set environment variables for unbuffered output and no pyc files
ENV PYTHONUNBUFFERED 1

# Copy requirements.txt to container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code to container
COPY . /app/

# The default command when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
