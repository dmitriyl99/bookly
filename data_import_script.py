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
    filepath = 'data/circulations.csv'
    if not os.path.exists(filepath):
        print('Circulation data not found')
        return
    df_circulations = pd.read_csv(filepath)
    df_circulations.drop(['Unnamed: 0'], axis=1, inplace=True)
    df_circulations.set_index('circulation_id', inplace=True)
    df_circulations = df_circulations[['reader_id', 'book_id']]
    print('Write circulations into database...')
    with engine.begin() as connection:
        df_circulations.to_sql('circulations', connection,
                               if_exists='append', index_label='id', chunksize=100)
    print('Done')


def import_books():
    print('Loading books...')
    filepath = 'data/books_alt.csv'
    if not os.path.exists(filepath):
        print('Books data not found')
        return
    df_books = pd.read_csv(filepath)
    df_books.set_index('id', inplace=True)
    df_books = df_books[['person', 'publicationType', 'language_id',
                         'material_id', 'rubric_id', 'author_id', 'serial_id']]
    print('Import books into database...')
    df_books['person'] = df_books['person'].astype(object)
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


if __name__ == '__main__':
    acceptable_args = ['circulations', 'books', 'readers']
    args = sys.argv
    if not args:
        args = acceptable_args
    else:
        for arg in args:
            if arg not in acceptable_args and arg != os.path.basename(__file__):
                raise ValueError('Invalid argument: %s' % arg)
    if 'readers' in args:
        import_readers()
    if 'books' in args:
        import_books()
    if 'circulations' in args:
        import_circulations()

