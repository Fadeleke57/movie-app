import os
from app import create_app
from app.utils.db import db

app = create_app()

def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully.")

def drop_db():
    """Drop the database tables."""
    with app.app_context():
        db.drop_all()
        print("Database tables dropped successfully.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Database Management Script")
    parser.add_argument(
        "command",
        choices=["init_db", "drop_db"],
        help="Command to execute: init_db (initialize the database), drop_db (drop all tables)."
    )

    args = parser.parse_args()

    if args.command == "init_db":
        init_db()
    elif args.command == "drop_db":
        drop_db()
