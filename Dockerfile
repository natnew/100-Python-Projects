# Use smaller slime image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (basic ones)
RUN apt-get update && apt-get install -y gcc

# Install Poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock* /app/

# Configure poetry to not use venv (container is already isolated)
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-interaction --no-ansi

# Copy the source code
COPY . /app

# Set PYTHONPATH to root so modules resolve correctly
ENV PYTHONPATH=/app

# Default command: Run the Omnibus Agent
CMD ["python", "Tier-3-Evaluation-and-Safety/100-Final-Omnibus-Agent/src/main.py"]
