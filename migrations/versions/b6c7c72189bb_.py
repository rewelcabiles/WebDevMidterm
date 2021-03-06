"""empty message

Revision ID: b6c7c72189bb
Revises: 198fb22d2382
Create Date: 2021-04-22 15:53:00.293480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6c7c72189bb'
down_revision = '198fb22d2382'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('admin', sa.Boolean(), nullable=False))
    op.add_column('user', sa.Column('register_date', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'register_date')
    op.drop_column('user', 'admin')
    # ### end Alembic commands ###
