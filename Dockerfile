# Use an official Python runtime as a parent image
FROM python:3.10.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Install Ollama
RUN curl https://ollama.ai/install.sh | sh

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PATH="/app:${PATH}"

# Optional: Set environment variables for Weaviate connection
# ENV WEAVIATE_HOST=http://localhost:8080
# ENV WEAVIATE_PORT=8080

# Expose port 80
EXPOSE 80

# Run database setup using docker-compose
# RUN docker compose up -d

# Setup Ollama and run LLM
#ENV LLM_NAME = $(cat config.yml | grep 'LLM' | cut -d' ' -f2)

#RUN ollama run LLM_NAME

# Define environment variable
ENV NAME CLI-RAG

# Run rag.py when the container launches
CMD ["python", "rag.py"]