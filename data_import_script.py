"""
Scrypt to import existing books, readers and circulations data to database

Start:
    python data_import_script.py

If any arguments are not provided, all data will be imported
Start partial:
    python data_import_script.py circulations
    python data_import_script.py readers
    python data_import_script.py books

You can provide several arguments
For example:
    python data_import_script.py readers books

All data must be in "data" folder in the root of the project:
data/circulations.csv
data/books.csv
data/readers.csv
"""

from app.data.database import engine
import pandas as pd
import sys
import os


def import_circulations():
    print('Loading circulations...')
    for i in range(1, 17):
        filepath = f'data/circulaton_{i}.csv'
        if not os.path.exists(filepath):
            print('Circulation data not found')
            return
        df_circulations = pd.read_csv(filepath)
        df_circulations.set_index('id', inplace=True)
        print('Write circulations into database...')
        with engine.begin() as connection:
            df_circulations.to_sql('circulations', connection,
                                   if_exists='append', index_label='id', chunksize=100)
    print('Done')


def import_books():
    print('Loading books...')
    filepath = 'data/books.csv'
    if not os.path.exists(filepath):
        print('Books data not found')
        return
    df_books = pd.read_csv(filepath)
    df_books.set_index('id', inplace=True)
    df_books.drop(['Unnamed: 0'], axis=1, inplace=True)
    df_books.rename(columns={'person': 'person_id'}, inplace=True)
    df_books.rename(columns={'publicationType': 'publication_type'}, inplace=True)
    print('Import books into database...')
    with engine.begin() as connection:
        df_books.to_sql('books', connection, if_exists='append', index_label='id', chunksize=100)
    print('Done')


def import_readers():
    print('Loading readers...')
    filepath = 'data/readers.csv'
    if not os.path.exists(filepath):
        print('Readers data not found')
        return
    df_readers = pd.read_csv(filepath)
    df_readers.drop(['Unnamed: 0'], axis=1, inplace=True)
    df_readers.set_index('reader_id', inplace=True)
    df_readers = df_readers.rename(columns={'dateOfBirth': 'date_of_birth'})
    df_readers.date_of_birth = pd.to_datetime(df_readers.date_of_birth)
    print('Import readers into database...')
    with engine.begin() as connection:
        df_readers.to_sql('readers', connection, if_exists='append', index_label='id')
    print('Done')


def import_authors():
    print('Loading authors...')
    filepath = 'data/authors.csv'
    if not os.path.exists(filepath):
        print('Authors data not found')
        return
    df_authors = pd.read_csv(filepath)
    df_authors.drop(['Unnamed: 0'], axis=1, inplace=True)
    df_authors.set_index('id', inplace=True)
    df_authors = df_authors.rename(columns={'author': 'name'})
    print('Import authors into database...')
    with engine.begin() as connection:
        df_authors.to_sql('authors', connection, if_exists='append', index_label='id')
    print('Done')


if __name__ == '__main__':
    acceptable_args = ['circulations', 'books', 'readers', 'authors']
    args = acceptable_args
    if len(sys.argv) > 1:
        args = sys.argv
        for arg in args:
            if arg not in acceptable_args and arg != os.path.basename(__file__):
                raise ValueError('Invalid argument: %s' % arg)
    if 'readers' in args:
        import_readers()
    if 'books' in args:
        import_books()
    if 'circulations' in args:
        import_circulations()
    if 'authors' in args:
        import_authors()

