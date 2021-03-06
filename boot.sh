#!/bin/bash
#/bin/bash -c "source venv/bin/activate"
/bin/bash -c ""gunicorn -b :5000 --access-logfile - --error-logfile - --worker-tmp-dir /dev/shm --workers=2 --threads=4 --worker-class eventlet -w 1 owl:app