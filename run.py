"""Entrypoint: create the app against a file-backed SQLite DB, seed it, and run."""
import os
from app import create_app
from app.db import seed

DB_PATH = os.environ.get("DB_PATH", "store.db")

app = create_app(DB_PATH)
seed(DB_PATH)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005, debug=False)
