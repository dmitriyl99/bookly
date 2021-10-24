from typing import Optional, Tuple, List

from app.data.repositories import ReadersRepository, BooksRepository, CirculationsRepository
from app.config import base_path

from .exceptions import ModelNotFoundError, ModelNotLoadedError

from lightfm import LightFM
import pandas as pd
import numpy as np

import pickle
import os


class RecommendationSystem:
    """
    Recommendation system core class
    Interface to interact with controllers
    """

    _model: LightFM
    _readers: ReadersRepository
    _books: BooksRepository
    _circulations: CirculationsRepository

    _model_loaded: bool = False

    def __init__(self,
                 readers: ReadersRepository,
                 books: BooksRepository,
                 circulations: CirculationsRepository):
        self._readers = readers
        self._books = books
        self._circulations = circulations
        self._load_model()

    def get_recommendations_for_reader(self, reader_id: Optional[int] = None, n_rec_items=5) -> Tuple[List[int], List[int]]:
        if not self._model_loaded:
            raise ModelNotLoadedError("Model not loaded. Please call RecommendationSystem._load_model() to load the "
                                      "model")
        reader = self._readers.get_reader_by_id(reader_id=reader_id)
        if reader:
            recommended_books, history = self._interact_with_unknown_reader(n_rec_items)
        else:
            recommended_books, history = self._interact_with_existing_reader(reader, n_rec_items)
        return recommended_books, history

    def _interact_with_existing_reader(self, reader, n_rec_items) -> Tuple[List[int], List[int]]:
        books_ids = self._books.get_all_books_ids()
        scores = pd.Series(self._model.predict(reader[0], np.arange(len(books_ids))))  # TODO: with item features?
        scores.index = books_ids
        scores = list(pd.Series(scores.sort_values(ascending=False).index))
        known_books = self._circulations.get_circulations_by_reader(reader[0])
        df_known_books = pd.DataFrame(known_books, columns=['circulation_id', 'reader_id', 'book_id'])
        known_books_ids = df_known_books.sort_values(by='book_id', ascending=False)
        scores = [x for x in scores if x not in known_books_ids]
        return scores[0:n_rec_items], known_books_ids

    def _interact_with_unknown_reader(self, n_rec_items) -> Tuple[List[int], List[int]]:
        return self._circulations.get_n_popular_books(n_rec_items), []

    def _load_model(self):
        """
        Load LightFM model from pickle file
        """
        if self._model_loaded:
            return
        model_directory = 'model'
        model_filename = 'model.pickle'
        model_fill_path = os.path.join(base_path, model_directory, model_filename)
        if not os.path.exists(model_fill_path):
            raise ModelNotFoundError("Model not found at path '%s'. Please put the model file into this directory"
                                     % model_fill_path)
        with open(model_fill_path, 'rb') as file:
            self._model = pickle.load(file)
        self._model_loaded = True
