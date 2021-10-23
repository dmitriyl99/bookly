from typing import List

from sqlalchemy.orm import Session

from app.data.tables import books


class BooksRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_books(self) -> List:
        return self.db.query(books).all()
