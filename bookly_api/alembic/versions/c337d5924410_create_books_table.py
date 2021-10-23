"""create books table

Revision ID: c337d5924410
Revises: 30f600e4a498
Create Date: 2021-10-20 23:30:56.298059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c337d5924410'
down_revision = '30f600e4a498'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'books',
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


def downgrade():
    op.drop_table('books')
