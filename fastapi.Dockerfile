# Use an official Python runtime as a parent image
FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory in the container
COPY ./src /app/src
COPY pyproject.toml /app
COPY uv.lock /app
WORKDIR /app

RUN uv sync --frozen --no-cache

# Define the command to run the application
CMD ["/app/.venv/bin/fastapi", "run", "src/api_server/main.py", "--port", "80", "--host", "0.0.0.0"]
