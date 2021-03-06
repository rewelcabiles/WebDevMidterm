"""empty message

Revision ID: 99bc9fffb346
Revises: e68c6e75b6b6
Create Date: 2021-05-10 20:38:12.698315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99bc9fffb346'
down_revision = 'e68c6e75b6b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('review_game_user',
    sa.Column('review_id', sa.Integer(), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['review_id'], ['review.id'], )
    )
    op.create_table('review_user',
    sa.Column('review_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['review_id'], ['review.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['app_user.id'], )
    )
    op.drop_table('review_game_tag')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('review_game_tag',
    sa.Column('review_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('game_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('app_user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['app_user_id'], ['app_user.id'], name='review_game_tag_app_user_id_fkey'),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], name='review_game_tag_game_id_fkey'),
    sa.ForeignKeyConstraint(['review_id'], ['review.id'], name='review_game_tag_review_id_fkey')
    )
    op.drop_table('review_user')
    op.drop_table('review_game_user')
    # ### end Alembic commands ###
