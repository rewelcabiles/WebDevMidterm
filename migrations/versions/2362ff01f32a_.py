"""empty message

Revision ID: 2362ff01f32a
Revises: fcaf64a304e1
Create Date: 2021-04-22 20:14:29.540154

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2362ff01f32a'
down_revision = 'fcaf64a304e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('password', sa.LargeBinary(length=90), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.Column('register_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.Column('password', postgresql.BYTEA(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=60), autoincrement=False, nullable=False),
    sa.Column('admin', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('register_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key'),
    sa.UniqueConstraint('username', name='user_username_key')
    )
    op.drop_table('app_user')
    # ### end Alembic commands ###
