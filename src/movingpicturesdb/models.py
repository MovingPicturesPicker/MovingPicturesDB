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
    rot_critics_score = Column(Integer, nullable=True)
    rot_audience_score = Column(Integer, nullable=True)
    user_score = Column(Integer, nullable=True)
    url = Column(String, nullable=True)
    insert_dt = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
