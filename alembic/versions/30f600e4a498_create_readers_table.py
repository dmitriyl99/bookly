"""create readers table

Revision ID: 30f600e4a498
Revises: 
Create Date: 2021-10-20 22:21:08.676067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30f600e4a498'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'readers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('date_of_birth', sa.Date, nullable=True)
    )


def downgrade():
    op.drop_table('readers')
