from datetime import date, datetime, timezone

from pydantic import BaseModel, Field


class MovingPicture(BaseModel):

    title: str
    released_date: date
    description: str | None = Field(default=None)
    critics_score: int | None = Field(default=None, ge=0, le=100)
    audience_score: int | None = Field(default=None, ge=0, le=100)
    user_score: int | None = Field(default=None, ge=0, le=100)
    # insert_dt: datetime = Field(default=datetime.now(timezone.utc))
    url: str | None = Field(default=None)
