from sqlalchemy.orm import Session

from app.data.tables import readers


class ReadersRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_reader_by_id(self, reader_id: int):
        return self.db.query(readers).where(readers.columns.id == reader_id).first()
