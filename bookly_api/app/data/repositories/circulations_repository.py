from typing import List

from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from app.data.tables import circulations


class CirculationsRepository:
    """
    Repository for circulations entities
    """

    def __init__(self, db: Session):
        self.db = db

    def get_circulations_by_reader(self, reader_id: int) -> List:
        """
        Get books history by reader

        :return: List
        """
        return self.db.query(circulations).where(circulations.columns.reader_id == reader_id).all()

    def get_n_popular_books(self, n) -> List[int]:
        result = self.db.query(circulations.columns.book_id, func.count(circulations.columns.id).label('count')) \
            .group_by(circulations.columns.book_id).order_by(desc('count')).limit(n).all()
        return [x[0] for x in result]
