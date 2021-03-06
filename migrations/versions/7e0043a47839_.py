"""empty message

Revision ID: 7e0043a47839
Revises: 87c36a0fa500
Create Date: 2021-05-10 21:03:37.001190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e0043a47839'
down_revision = '87c36a0fa500'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('game', 'rating')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('game', sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
