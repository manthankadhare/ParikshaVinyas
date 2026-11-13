import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from scripts.seed_database import seed

def reset():
    app = create_app()
    with app.app_context():
        print("Dropping all existing database tables...")
        db.drop_all()
        print("Tables dropped.")
        seed()

if __name__ == '__main__':
    reset()

