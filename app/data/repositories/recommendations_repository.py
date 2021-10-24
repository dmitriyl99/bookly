from sqlalchemy.orm import Session

from app.data.tables import recommendations
from app.data.database import engine


class RecommendationsRepository:
    _db: Session

    def __init__(self, db: Session):
        self._db = db

    def save_recommendations_for_reader(self, reader_id: int, books_ids: list):
        delete_query = recommendations.delete().where(recommendations.c.reader_id == reader_id)
        engine.execute(delete_query)
        for book_id in books_ids:
            query = recommendations.insert().values(reader_id=reader_id, book_id=book_id)
            engine.execute(query)

    def get_recommendations_by_reader_id(self, reader_id: int):
        return self._db.query(recommendations).filter(recommendations.c.reader_id == reader_id).all()
