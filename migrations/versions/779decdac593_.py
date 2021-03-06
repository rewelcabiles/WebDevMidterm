"""empty message

Revision ID: 779decdac593
Revises: d51b2822af88
Create Date: 2021-05-08 18:27:09.939337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '779decdac593'
down_revision = 'd51b2822af88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('game', 'rating',
               existing_type=sa.NUMERIC(precision=2, scale=1),
               type_=sa.Integer(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('game', 'rating',
               existing_type=sa.Integer(),
               type_=sa.NUMERIC(precision=2, scale=1),
               existing_nullable=True)
    # ### end Alembic commands ###
