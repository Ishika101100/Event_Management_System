"""empty message

Revision ID: 31042c99f7d9
Revises: da91fbc5d204
Create Date: 2022-06-16 17:02:54.614892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31042c99f7d9'
down_revision = 'da91fbc5d204'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_type', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_type')
    )
    op.drop_column('user', 'is_admin')
    op.drop_column('user', 'gender')
    op.drop_column('user', 'age')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('gender', sa.VARCHAR(length=10), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('is_admin', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_table('user_type')
    # ### end Alembic commands ###