"""Entrypoint: create the app against a file-backed SQLite DB, seed it, and run."""
import os
from app import create_app
from app.db import seed

DB_PATH = os.environ.get("DB_PATH", "store.db")
HOST = os.environ.get("HOST", "0.0.0.0")  # 0.0.0.0 = reachable from other devices on the LAN
PORT = int(os.environ.get("PORT", "5005"))

app = create_app(DB_PATH)
seed(DB_PATH)

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=False)
