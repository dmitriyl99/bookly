"""Create recommendations table

Revision ID: fa399e706820
Revises: c6ff4b76e2fa
Create Date: 2021-10-24 11:37:43.400840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa399e706820'
down_revision = 'c6ff4b76e2fa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'recommendations',
        sa.Column('reader_id', sa.Integer, nullable=True),
        sa.Column('book_id', sa.Integer),
    )


def downgrade():
    op.drop_table('recommendations')
