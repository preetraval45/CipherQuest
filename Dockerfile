FROM python:3.11-slim-bookworm

# Update package lists, install security updates, and clean up in a single RUN instruction
RUN apt-get update && apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

WORKDIR /app

