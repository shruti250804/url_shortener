from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models import URL
from app.schemas import URLCreate
import random
import string
from fastapi.responses import RedirectResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "URL Shortener API Running"}


@app.post("/shorten")
def shorten_url(url: URLCreate, db: Session = Depends(get_db)):

    short_code = ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=6
        )
    )

    new_url = URL(
        original_url=url.original_url,
        short_code=short_code
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return {
        "short_code": short_code,
        "original_url": url.original_url
    }

@app.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):

    url = db.query(URL).filter(
        URL.short_code == short_code
    ).first()

    if not url:
        return {"error": "URL not found"}

    url.clicks += 1
    db.commit()

    return RedirectResponse(url.original_url)