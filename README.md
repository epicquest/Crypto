# Crypto FastAPI Application

A FastAPI-based application that interacts with a PostgreSQL database to manage cryptocurrency data. This project uses SQLAlchemy ORM and asyncpg for PostgreSQL integration, providing a simple and scalable way to store, retrieve, and manage cryptocurrency information.

## Features

- **CRUD Operations**: Perform Create, Read, Update, and Delete operations on cryptocurrency data.
- **Async Database**: Utilizes asynchronous database connections using `asyncpg` and SQLAlchemy's async support.
- **FastAPI**: A modern web framework for building APIs with Python 3.7+ based on Starlette and Pydantic.

## Requirements

- Python 3.12+
- Docker (for running the PostgreSQL container)
- PostgreSQL 12+ (the database is run using Docker)

## Installation

### Prerequisites

1. Clone the repository:
   ```bash
   git clone https://github.com/epicquest/Crypto.git
   cd Crypto

