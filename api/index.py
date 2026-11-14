import sys
import os

# Insert project root into sys.path so app and config can be imported on Vercel
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from run import app

# Vercel serverless WSGI entrypoint
app.debug = False
