from typing import List, Generator

from sqlalchemy.orm import Session

from app.data.tables import books


class BooksRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_books(self) -> List:
        return self.db.query(books).all()

    def get_all_books_ids(self) -> List[int]:
        result = self.db.query(books.columns.id).order_by(books.columns.id).all()
        return [i[0] for i in result]
