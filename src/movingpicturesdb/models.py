from datetime import date, datetime, timezone

import sqlalchemy
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import DATE, TIMESTAMP

from movingpicturesdb.database import Base


class MovingPicture(Base):
    __tablename__ = "moving_pictures"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(250), nullable=False)
    released_date = Column(DATE)
    description = Column(String(1000), nullable=True)
    critics_score = Column(Integer, nullable=True)
    audience_score = Column(Integer, nullable=True)
    user_score = Column(Integer, nullable=True)
    url = Column(String, nullable=True)
    insert_dt = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


"""
CREATE TABLE MovingPicture (
    id serial PRIMARY KEY,
    title VARCHAR(250) NOT NULL,
    released_date DATE NOT NULL,
    description VARCHAR(1000) NULL,
    critics_score SMALLINT NULL,
    audience_score SMALLINT NULL,
    user_score SMALLINT NULL,
    url VARCHAR NULL
);
"""


"""
INSERT INTO moving_pictures (title, released_date, critics_score, audience_score) 
VALUES
    ('Jeanne du Barry', '2024-05-02', 46, 94),
    ('The Fall Guy', '2024-05-03', 83, 87),
    ('New Life', '2024-05-03', 95, 85)
"""
