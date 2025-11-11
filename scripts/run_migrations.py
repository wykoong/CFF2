# Simple runner to apply SQL migrations in .specify/db/migrations
import os
import sys
from pathlib import Path

# Add the project root to Python path
root = Path(__file__).resolve().parents[1]
sys.path.append(str(root))

from src.dao import apply_migrations

if __name__ == "__main__":
    apply_migrations()
    print("Migrations applied.")