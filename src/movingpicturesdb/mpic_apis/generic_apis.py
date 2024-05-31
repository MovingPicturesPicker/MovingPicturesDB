import time

import psycopg
from fastapi import Depends, FastAPI, HTTPException, Response, status
from movingpicturesdb import database as DB
from movingpicturesdb import models, schemas
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
async def get_all_movies(db: Session = Depends(DB.get_db)):
    """Get all Moving Picture entries"""
    all_movies = db.query(models.MovingPicture).all()
    return all_movies


@mpic.get(
    "/movies/latest",
    response_model=schemas.MovingPictureResponse,
)
async def get_latest_movie(db: Session = Depends(DB.get_db)):
    """Get the most recently added movie."""
    qs_movies = db.query(models.MovingPicture).order_by(models.MovingPicture.id.desc())
    last_movie = qs_movies.first()

    return last_movie


@mpic.get(
    "/movies/{id}",
    response_model=schemas.MovingPictureResponse,
)
async def get_movie(id: int, db: Session = Depends(DB.get_db)):
    """Get a single movie entry, using the movie's PK."""
    qs_movies = db.query(models.MovingPicture).filter(models.MovingPicture.id == id)

    movie = qs_movies.first()
    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Retrieval Failed. Movie {id} was not found.",
        )
    return movie


@mpic.post(
    "/new-movie",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.MovingPictureResponse,
)
async def create_movie(
    movie: schemas.CreateMovingPicture,
    db: Session = Depends(DB.get_db),
):
    """Adds new entry in the the MovingPicture Table"""
    print(movie.model_dump())
    new_movie = models.MovingPicture(**movie.model_dump())

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)

    return new_movie


@mpic.put(
    "/movies/{id}",
    response_model=schemas.MovingPictureResponse,
)
async def update_movie(
    id: int,
    updated_movie: schemas.CreateMovingPicture,
    db: Session = Depends(DB.get_db),
):
    qs_movies = db.query(models.MovingPicture).filter(models.MovingPicture.id == id)
    if qs_movies.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Update Failed. Movie {id} was not found.",
        )

    qs_movies.update(updated_movie.model_dump(), synchronize_session=False)
    db.commit()

    return qs_movies.first()


@mpic.delete(
    "/movies/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_movie(id: int, db: Session = Depends(DB.get_db)):
    """Remove a single movie entry from the DB, using the movie's PK."""
    qs_movies = db.query(models.MovingPicture).filter(models.MovingPicture.id == id)
    mov_to_del = qs_movies.first()
    if mov_to_del is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deletion Failed. Movie {id} was not found.",
        )
    qs_movies.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
