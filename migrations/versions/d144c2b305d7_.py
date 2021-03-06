"""empty message

Revision ID: d144c2b305d7
Revises: 497a5bd0cea8
Create Date: 2021-05-05 13:13:45.255913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd144c2b305d7'
down_revision = '497a5bd0cea8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('platform', 'available',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('platform', 'name',
               existing_type=sa.VARCHAR(length=60),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('platform', 'name',
               existing_type=sa.VARCHAR(length=60),
               nullable=False)
    op.alter_column('platform', 'available',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###
