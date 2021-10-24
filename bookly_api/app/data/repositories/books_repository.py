from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.data.tables import books, authors


class BooksRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_books(self) -> List:
        return self.db.query(books).all()

    def get_all_books_ids(self) -> List[int]:
        result = self.db.query(books.columns.id).order_by(books.columns.id).all()
        return [i[0] for i in result]

    def get_book_by_id(self, book_id: int) -> Optional[Tuple]:
        return self.db.query(books).get(book_id)

    def get_books_by_ids(self, book_ids: list) -> List[Tuple]:
        return self.db.query(books.columns.id, books.columns.title, authors.columns.name)\
            .join(authors, books.columns.author_id == authors.columns.id, isouter=True)\
            .filter(books.columns.id.in_(tuple(book_ids)))\
            .all()
