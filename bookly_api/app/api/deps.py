from typing import Generator

from fastapi import Depends

from sqlalchemy.orm import Session

from app.data.database import SessionLocal
from app.data.repositories import BooksRepository, CirculationsRepository, ReadersRepository
from app.core.recommendation import RecommendationSystem


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_readers_repository(db: Session = Depends(get_db)) -> ReadersRepository:
    return ReadersRepository(db)


def get_books_repository(db: Session = Depends(get_db)) -> BooksRepository:
    return BooksRepository(db)


def get_circulations_repository(db: Session = Depends(get_db)) -> CirculationsRepository:
    return CirculationsRepository(db)


def get_recommendation_service(readers_repository: ReadersRepository = Depends(get_readers_repository),
                               books_repository: BooksRepository = Depends(get_books_repository),
                               circulations_repository: CirculationsRepository = Depends(get_circulations_repository)):
    return RecommendationSystem(readers=readers_repository,
                                books=books_repository,
                                circulations=circulations_repository)
