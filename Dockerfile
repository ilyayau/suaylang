# syntax=docker/dockerfile:1
FROM python:3.12-slim

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    make \
    bash \
    zsh \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /workspace

# Copy rest of the code
COPY . .

# Install (editable) with required extras
RUN pip install --upgrade pip && \
    pip install -e ".[dev,plots]"

# Default shell is bash for scripts
SHELL ["/bin/bash", "-c"]

# Environment: force UTF-8, set Python path
ENV PYTHONUTF8=1
ENV PYTHONPATH=/workspace

# Entrypoint for artifact reproduction
ENTRYPOINT ["/bin/bash", "./scripts/reproduce.sh"]
