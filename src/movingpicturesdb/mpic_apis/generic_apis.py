import time

import psycopg
from fastapi import Depends, FastAPI, HTTPException, Response, status
from movingpicturesdb import database as DB
from movingpicturesdb import models, schemas
from movingpicturesdb.dummy_movies import movies
from psycopg.rows import dict_row
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=DB.engine)

mpic = FastAPI()


while True:
    try:
        connection = psycopg.connect(
            host="localhost",
            port=5432,
            dbname="mpictures-db",
            user="mpictures-db",
            password="^$RBFC4b5d",
            row_factory=dict_row,
        )
        cursor = connection.cursor()
        print("DB connection was successful!")
        break

    except Exception as exc:
        print("Connection failed.")
        print("Error", exc)
        time.sleep(2)


def find_moving_pic(movie_id: int) -> dict | None:
    "Find a moving picture."
    for movie in movies:
        if not movie["id"] == movie_id:
            continue
        return movie


@mpic.get("/test_db")
async def test_dp(db: Session = Depends(DB.get_db)):
    """Get all Moving Picture entries"""
    all_movies = db.query(models.MovingPicture).all()
    return {"data": all_movies}


@mpic.get("/movie/latest")
async def get_latest_movie():
    """Get the most recently added movie."""
    movie = movies[-1]
    return movie


@mpic.get("/movie/{id}")
async def get_movie(id: int, response=Response):
    """Get a single movie entry, using the movie's PK."""
    movie = find_moving_pic(movie_id=id)
    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No movie could be found."
        )
    return {"data": movie}


@mpic.post("/new-movie", status_code=status.HTTP_201_CREATED)
async def create_movie(
    movie: schemas.MovingPicture,
    db: Session = Depends(DB.get_db),
):
    """Adds new entry in the the MovingPicture Table"""
    print(movie.model_dump())
    new_movie = models.MovingPicture(**movie.model_dump())

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)

    return {"data": new_movie}


@mpic.delete("/movie/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(id: int, response: Response):
    """Remove a single movie entry from the DB, using the movie's PK."""
    movie = find_moving_pic(movie_id=id)
    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No movie could be found."
        )
    movies.remove(movie)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
