# Use the official Python image as base
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Command to run the Celery worker
CMD ["celery", "-A", "celery_worker.celery_app", "worker", "--loglevel=info"]
