import os
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from models import Base

# Import your SQLAlchemy Base

# Load Alembic configuration
config = context.config

# Apply logging configuration
if config.config_file_name:
    fileConfig(config.config_file_name)

# Set database URL dynamically

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://test_user:Hdre83gr765fg344ddD33@localhost:5432/crypto_db")

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Metadata for autogenerate feature
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(url=DATABASE_URL, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
