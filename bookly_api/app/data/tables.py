import sqlalchemy as sa

from .database import metadata


books = sa.Table(
    'books',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('author_id', sa.Integer),
    sa.Column('rubric_id', sa.Integer),
    sa.Column('rubric_parent_id', sa.Integer),
    sa.Column('language_id', sa.Integer),
    sa.Column('material_id', sa.Integer),
    sa.Column('person_id', sa.Integer),
    sa.Column('serial_id', sa.Integer),
    sa.Column('smart_collapse_field', sa.String, nullable=True),
    sa.Column('publication_type', sa.String),
)

circulations = sa.Table(
    'circulations',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('reader_id', sa.Integer, index=True),
    sa.Column('book_id', sa.Integer, index=True)
)

readers = sa.Table(
    'readers',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('date_of_birth', sa.Date, nullable=True),
    sa.Column('address', sa.String, nullable=True)
)
