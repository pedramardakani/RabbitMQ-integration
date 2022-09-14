# Follow the builder pattern and cache the 'base' image
FROM python:3.10-slim-bullseye AS base

WORKDIR /app

# Follow the Principle of Least Privilege and create a non-root user
RUN useradd -ms /bin/sh captain

USER captain

# Install and cache dependencies
COPY --chown=captain:captain requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port to communicate with RabbitMQ
EXPOSE 5672

FROM base AS prod