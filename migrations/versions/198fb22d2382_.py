"""empty message

Revision ID: 198fb22d2382
Revises: f977edd13cd0
Create Date: 2021-04-22 00:38:02.182815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '198fb22d2382'
down_revision = 'f977edd13cd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.String(length=60), nullable=False))
    op.create_unique_constraint(None, 'user', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'email')
    # ### end Alembic commands ###