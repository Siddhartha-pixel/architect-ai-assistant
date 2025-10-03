# backend/alembic/env.py

import os
import re
from logging.config import fileConfig
import sys
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# --- NEW CODE BLOCK TO FIX 'ModuleNotFoundError' ---
# Add the parent directory of 'alembic' (which is our main /app folder)
# to the Python path.
sys.path.append(str(Path(__file__).resolve().parents[1]))
# --- END OF NEW CODE BLOCK ---


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# --- START OF CUSTOM DEBUGGING AND CONFIGURATION CODE ---
print("--- Running custom alembic/env.py configuration ---")
try:
    # Manually find and parse the .env file
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    print(f"Attempting to find .env file at: {dotenv_path}")
    
    db_url = None
    if os.path.exists(dotenv_path):
        print("SUCCESS: .env file was found.")
        with open(dotenv_path, 'r') as f:
            for line in f:
                match = re.search(r'^\s*DATABASE_URL\s*=\s*(.*)', line)
                if match:
                    db_url = match.group(1).strip()
                    print("SUCCESS: Found DATABASE_URL in .env file.")
                    break
    else:
        print("ERROR: .env file was NOT found at the specified path.")

    if db_url:
        print("Setting sqlalchemy.url in config.")
        config.set_main_option('sqlalchemy.url', db_url)
    else:
        print("FATAL ERROR: DATABASE_URL could not be found in the .env file.")
        raise ValueError("DATABASE_URL not configured in .env file")

except Exception as e:
    print(f"An unexpected error occurred during configuration: {e}")
    raise e
print("--- Finished custom configuration ---")
# --- END OF CUSTOM DEBUGGING AND CONFIGURATION CODE ---


# We are commenting this out to avoid the 'formatters' error
#if config.config_file_name is not None:
#    fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
from app.database import Base
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
    run_migrations_online()