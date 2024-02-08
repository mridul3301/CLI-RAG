# Use an official Python runtime as a parent image
FROM python:3.10.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Docker Compose
RUN apt-get update && \
    apt-get install -y docker-compose && \
    rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl https://ollama.ai/install.sh | sh

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PATH="/app:${PATH}"

# Run database setup using docker-compose
RUN docker compose up -d

# Setup Ollama and run LLM
RUN ollama run $(cat config.yml | grep 'LLM' | cut -d' ' -f2)

# Define environment variable
ENV NAME CLI-RAG

# Run rag.py when the container launches
CMD ["python", "rag.py"]