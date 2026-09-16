# URL Shortener Service

A backend URL shortening service built using FastAPI, PostgreSQL, and SQLAlchemy.

## Features
- Create short URLs
- Redirect to original URLs
- Click tracking
- PostgreSQL database integration
- Swagger API documentation

## Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic

## Run Locally

pip install -r requirements.txt

uvicorn app.main:app --reload