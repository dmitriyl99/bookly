from typing import Generator

from fastapi import Depends

from sqlalchemy.orm import Session

from app.data.database import SessionLocal
from app.data.repositories.readers_repository import ReadersRepository


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_readers_repository(db: Session = Depends(get_db)) -> ReadersRepository:
    return ReadersRepository(db)
