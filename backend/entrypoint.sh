#!/bin/sh
# Docker entrypoint script

# Run Django migrations
python src/db/manage.py migrate

# Start the FastAPI server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
