from typing import Optional, Tuple, List

from app.data.repositories import ReadersRepository, CirculationsRepository, RecommendationsRepository


class RecommendationSystem:
    """
    Recommendation system core class
    Interface to interact with controllers
    """

    _readers: ReadersRepository
    _circulations: CirculationsRepository
    _recommendations: RecommendationsRepository

    def __init__(self,
                 readers: ReadersRepository,
                 circulations: CirculationsRepository,
                 recommendations: RecommendationsRepository):
        self._readers = readers
        self._circulations = circulations
        self._recommendations = recommendations

    def get_recommendations_for_reader(self, reader_id: Optional[int] = None) -> Tuple[List[int], List[int]]:
        reader = None
        if reader_id:
            reader = self._readers.get_reader_by_id(reader_id=reader_id)
        if reader:
            recommended_books, history = self._interact_with_existing_reader(reader)

        else:
            recommended_books, history = self._interact_with_unknown_reader()
        return recommended_books, history

    def _interact_with_existing_reader(self, reader) -> Tuple[List[int], List[int]]:
        recommended_books = self._recommendations.get_recommendations_by_reader_id(reader[0])
        known_books = self._circulations.get_circulations_by_reader(reader[0])
        recommended_books_ids = [x[1] for x in recommended_books]
        known_books_ids = [x[1] for x in known_books]
        return recommended_books_ids, known_books_ids

    def _interact_with_unknown_reader(self, n_rec_items=5) -> Tuple[List[int], List[int]]:
        return self._circulations.get_n_popular_books(n_rec_items), []
