web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --host 0.0.0.0 --port 8000 --reload
worker: python worker.py
