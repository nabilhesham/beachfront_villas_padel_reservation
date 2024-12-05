#!/bin/bash

# Wait for the database to be ready (if needed)
# sleep 10  # Uncomment and adjust if your DB needs time to start

# Run the create_users command to ensure users are created
python manage.py create_users

# Run the default Django command (or any other command)
exec "$@"