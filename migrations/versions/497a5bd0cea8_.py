"""empty message

Revision ID: 497a5bd0cea8
Revises: 06a3b333c4b3
Create Date: 2021-05-05 13:09:48.843081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '497a5bd0cea8'
down_revision = '06a3b333c4b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('platform', sa.Column('available', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('platform', 'available')
    # ### end Alembic commands ###