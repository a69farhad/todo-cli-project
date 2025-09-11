# Minimal image using official Python
FROM python:3.10-slim

# App directory
WORKDIR /app

# Copy only what's needed for runtime
COPY todo.py /app/todo.py

# Create the data directory (will be bind-mounted for persistence)
RUN mkdir -p /app/data

# Default entrypoint so you can do:
#   docker run --rm todo-cli add "Read a book"
ENTRYPOINT ["python3", "/app/todo.py"]
