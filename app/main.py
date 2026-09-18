from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta
import random
import string

from app.database import Base, engine, get_db
from app.models import URL
from app.schemas import URLCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "URL Shortener API Running"}


@app.post("/shorten")
def shorten_url(url: URLCreate, db: Session = Depends(get_db)):

    if url.custom_code:
        short_code = url.custom_code
    else:
        short_code = ''.join(
            random.choices(
                string.ascii_letters + string.digits,
                k=6
            )
        )

    existing = db.query(URL).filter(
        URL.short_code == short_code
    ).first()

    if existing:
        return {
            "error": "Short code already exists"
        }

    expires_at = None

    if url.expires_in_days:
        expires_at = datetime.utcnow() + timedelta(
            days=url.expires_in_days
        )

    new_url = URL(
        original_url=str(url.original_url),
        short_code=short_code,
        expires_at=expires_at
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return {
        "short_code": short_code,
        "original_url": str(url.original_url),
        "expires_at": expires_at
    }


@app.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):

    url = db.query(URL).filter(
        URL.short_code == short_code
    ).first()

    if not url:
        return {
            "error": "URL not found"
        }

    if url.expires_at and datetime.utcnow() > url.expires_at:
        return {
            "error": "Link expired"
        }

    url.clicks += 1
    db.commit()

    return RedirectResponse(
        url=url.original_url,
        status_code=302
    )


@app.get("/analytics/{short_code}")
def get_analytics(
    short_code: str,
    db: Session = Depends(get_db)
):

    url = db.query(URL).filter(
        URL.short_code == short_code
    ).first()

    if not url:
        return {
            "error": "URL not found"
        }

    return {
        "original_url": url.original_url,
        "short_code": url.short_code,
        "clicks": url.clicks,
        "created_at": url.created_at,
        "expires_at": url.expires_at
    }