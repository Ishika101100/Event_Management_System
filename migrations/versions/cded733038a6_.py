"""empty message

Revision ID: cded733038a6
Revises: 1dfedcf64719
Create Date: 2022-07-06 12:18:55.449816

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cded733038a6'
down_revision = '1dfedcf64719'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'date')
    op.drop_column('event', 'time')
    op.drop_column('event', 'duration')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('duration', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.add_column('event', sa.Column('time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.add_column('event', sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###