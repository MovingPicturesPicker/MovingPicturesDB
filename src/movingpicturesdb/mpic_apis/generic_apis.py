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


@mpic.get("/movies/all")
async def get_all_movies(db: Session = Depends(DB.get_db)) -> dict:
    """Get all Moving Picture entries"""
    all_movies = db.query(models.MovingPicture).all()
    return {"data": all_movies}


@mpic.get("/movies/latest")
async def get_latest_movie() -> dict:
    """Get the most recently added movie."""
    movie = movies[-1]
    return movie


@mpic.get("/movies/{id}")
async def get_movie(id: int, db: Session = Depends(DB.get_db)) -> dict:
    """Get a single movie entry, using the movie's PK."""
    movie = db.query(models.MovingPicture).filter(models.MovingPicture.id == id).first()
    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No movie could be found."
        )
    return {"data": movie}


@mpic.post("/new-movie", status_code=status.HTTP_201_CREATED)
async def create_movie (
    movie: schemas.MovingPicture,
    db: Session = Depends(DB.get_db),
) -> dict:
    """Adds new entry in the the MovingPicture Table"""
    print(movie.model_dump())
    new_movie = models.MovingPicture(**movie.model_dump())

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)

    return {"data": new_movie}


@mpic.update("/movies/{id}")
async def update_movie(id:int, db: Session = Depends(DB.get_db)) -> dict:



@mpic.delete("/movies/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(id: int, db: Session = Depends(DB.get_db)) -> dict:
    """Remove a single movie entry from the DB, using the movie's PK."""
    movie = movie = db.query(models.MovingPicture).filter(models.MovingPicture.id == id)
    if movie.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No movie could be found."
        )
    movie.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
