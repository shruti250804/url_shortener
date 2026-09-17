# URL Shortener Service

A FastAPI-based URL shortening service with PostgreSQL integration.

## Features

- Create short URLs
- Redirect using short codes
- Track click counts
- PostgreSQL database
- SQLAlchemy ORM
- Swagger API Documentation

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Uvicorn

## Run Locally

pip install -r requirements.txt

uvicorn app.main:app --reload