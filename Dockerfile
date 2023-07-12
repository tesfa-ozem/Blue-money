# Use a Python base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the working directory
COPY Pipfile Pipfile.lock /app/

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential

# Install Pipenv
RUN pip install --upgrade pip && \
    pip install pipenv

# Install application dependencies
RUN pipenv install --deploy --system

# Copy the application code to the working directory
COPY . /app

# Expose the application port
EXPOSE 8000

# Start the FastAPI server
CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
