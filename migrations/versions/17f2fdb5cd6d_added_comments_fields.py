"""added comments fields

Revision ID: 17f2fdb5cd6d
Revises: f80b7c94ec40
Create Date: 2022-02-13 21:02:16.575941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17f2fdb5cd6d'
down_revision = 'f80b7c94ec40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('comment', sa.Text(), nullable=False))
    op.alter_column('comments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('comments', 'pitch_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_index('ix_comments_post_comment', table_name='comments')
    op.drop_column('comments', 'date')
    op.drop_column('comments', 'time')
    op.drop_column('comments', 'post_comment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('post_comment', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('comments', sa.Column('time', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('comments', sa.Column('date', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_index('ix_comments_post_comment', 'comments', ['post_comment'], unique=False)
    op.alter_column('comments', 'pitch_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('comments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('comments', 'comment')
    # ### end Alembic commands ###
