"""Create Authors Table

Revision ID: c6ff4b76e2fa
Revises: efbdf6bcacdf
Create Date: 2021-10-24 06:28:46.979810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6ff4b76e2fa'
down_revision = 'efbdf6bcacdf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'authors',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String)
    )


def downgrade():
    op.drop_table('authors')
