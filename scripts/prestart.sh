#! /usr/bin/env bash

set -e
set -x

# Let DB start
python backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python initial_data.py

# Start the main process
exec "$@"
