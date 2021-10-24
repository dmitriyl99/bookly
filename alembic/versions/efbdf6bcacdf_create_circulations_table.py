"""create circulations table

Revision ID: efbdf6bcacdf
Revises: c337d5924410
Create Date: 2021-10-20 23:31:02.374657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efbdf6bcacdf'
down_revision = 'c337d5924410'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'circulations',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('reader_id', sa.Integer, index=True),
        sa.Column('book_id', sa.Integer, index=True)
    )


def downgrade():
    op.drop_table('circulations')
