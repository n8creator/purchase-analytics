# Use the official Python 3.12 slim-buster image
FROM python:3.12-slim-buster

# Set the working directory in the container
WORKDIR /app

# Add user that will be used in the container
RUN useradd appuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.7.1
ENV POETRY_CACHE_DIR="/var/cache/pypoetry"
ENV PORT=8000

# Install system dependencies
# 'postgresql-client' required to run './manage dbshell' command
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    postgresql-client \
    neovim \
    tree \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml /app/

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

# Copy the project
COPY . .

# Change ownership of the app directory
RUN chown appuser:appuser /app

# Use user "appuser" to run the server
USER appuser

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Expose the port the app runs on
EXPOSE 8000

# Run the Django server
CMD ["gunicorn", "producer.wsgi:application", "--bind", "0.0.0.0:8000"]