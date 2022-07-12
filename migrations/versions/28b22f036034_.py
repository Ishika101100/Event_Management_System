"""empty message

Revision ID: 28b22f036034
Revises: a21028e332ad
Create Date: 2022-07-08 15:45:20.304815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28b22f036034'
down_revision = 'a21028e332ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'Total_charge')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('Total_charge', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
