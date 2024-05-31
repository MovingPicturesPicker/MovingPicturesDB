from datetime import date, datetime, timezone

from pydantic import BaseModel, Field


class BaseMovingPicture(BaseModel):
    title: str
    released_date: date
    description: str | None = Field(default=None)
    rot_critics_score: int | None = Field(default=None, ge=0, le=100)
    rot_audience_score: int | None = Field(default=None, ge=0, le=100)
    url: str | None = Field(default=None)


class CreateMovingPicture(BaseMovingPicture):
    pass


class MovingPictureResponse(BaseModel):
    title: str
    released_date: date
    description: str | None = Field(default=None)

    class Config:
        from_attributes = True
