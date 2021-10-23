from typing import Optional

from app.data.repositories import ReadersRepository, BooksRepository, CirculationsRepository


class RecommendationSystem:
    """
    Recommendation system core class
    Interface to interact with controllers
    """

    def __init__(self,
                 readers: ReadersRepository,
                 books: BooksRepository,
                 circulations: CirculationsRepository):
        self.readers = readers
        self.books = books
        self.circulations = circulations

    def get_recommendations_for_reader(self, reader_id: Optional[int] = None):
        reader = self.readers.get_reader_by_id(reader_id=reader_id)
        if not reader:
            # Interact with non readers - recommend most popular books
            pass

