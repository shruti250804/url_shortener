from pydantic import BaseModel, HttpUrl
from datetime import datetime


class URLCreate(BaseModel):
    original_url: HttpUrl


class URLResponse(BaseModel):
    short_code: str
    original_url: str


class AnalyticsResponse(BaseModel):
    original_url: str
    short_code: str
    clicks: int
    created_at: datetime