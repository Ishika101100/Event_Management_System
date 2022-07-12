"""empty message

Revision ID: 40be6bfedc23
Revises: 4c3c257c9233
Create Date: 2022-07-06 14:08:11.977986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40be6bfedc23'
down_revision = '4c3c257c9233'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('start_time', sa.Time(), nullable=False))
    op.add_column('event', sa.Column('end_time', sa.Time(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'end_time')
    op.drop_column('event', 'start_time')
    # ### end Alembic commands ###