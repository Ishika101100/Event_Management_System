"""empty message

Revision ID: 8035b8b4e955
Revises: 0679d59f15b9
Create Date: 2022-07-08 16:04:29.286515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8035b8b4e955'
down_revision = '0679d59f15b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('Total_charge', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'Total_charge')
    # ### end Alembic commands ###