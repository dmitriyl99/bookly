import os
import pickle
from typing import Optional

import pandas as pd
import numpy as np
from lightfm import LightFM
import scipy.sparse

from app.config import base_path
from app.core.exceptions import ModelNotFoundError
from app.data.database import engine, SessionLocal
from app.data.repositories import BooksRepository, CirculationsRepository, RecommendationsRepository


def generate_int_id(dataframe, id_col_name):
    new_dataframe=dataframe.assign(
        int_id_col_name=np.arange(len(dataframe))
        ).reset_index(drop=True)
    return new_dataframe.rename(columns={'int_id_col_name': id_col_name})


def generate_recommendations():
    n_rec_items = 5
    print('Load data')
    df_readers = _load_readers()
    df_readers = generate_int_id(df_readers, 'readers_id_num')

    db = SessionLocal()
    books = BooksRepository(db)
    circulations = CirculationsRepository(db)
    recommendations = RecommendationsRepository(db)

    print('Load model')
    model = _load_model()
    features = _load_features()

    books_ids = books.get_all_books_ids()
    books_id_nums = np.arange(len(books_ids))
    print(len(books_id_nums))
    print(books_id_nums.max())
    print('Start generation recommendations')
    for _, df_reader in df_readers.iterrows():
        reader_id = df_reader['readers_id_num']
        scores = pd.Series(model.predict(reader_id, books_id_nums, item_features=features))
        scores.index = books_ids
        scores = list(pd.Series(scores.sort_values(ascending=False).index))
        known_books = circulations.get_circulations_by_reader(df_reader['id'])
        df_known_books = pd.DataFrame(known_books, columns=['circulation_id', 'reader_id', 'book_id'])
        known_books_ids = df_known_books.sort_values(by='book_id', ascending=False)
        scores = [x for x in scores if x not in known_books_ids]
        recommended_books = scores[0:n_rec_items]
        recommendations.save_recommendations_for_reader(df_reader['id'], recommended_books)
    print('Done')


def _load_readers() -> pd.DataFrame:
    return pd.read_sql('SELECT * FROM readers ORDER BY id DESC', engine)


def _load_model() -> LightFM:
    """
    Load LightFM model from pickle file
    """
    model_directory = 'model'
    model_filename = 'model.pickle'
    model_full_path = os.path.join(base_path, model_directory, model_filename)
    if not os.path.exists(model_full_path):
        raise ModelNotFoundError("Model not found at path '%s'. Please put the model file into this directory"
                                 % model_full_path)
    with open(model_full_path, 'rb') as file:
        return pickle.load(file)


def _load_features():
    model_directory = 'model'
    features_files = 'books_features.npz'
    features_full_path = os.path.join(base_path, model_directory, features_files)
    if os.path.exists(features_full_path):
        return scipy.sparse.load_npz(features_full_path)
    print('Features not found at path "%s"' % features_full_path)
    return None


if __name__ == '__main__':
    generate_recommendations()
