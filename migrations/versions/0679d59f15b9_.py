"""empty message

Revision ID: 0679d59f15b9
Revises: 548a569a43f5
Create Date: 2022-07-08 16:02:18.479364

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0679d59f15b9'
down_revision = '548a569a43f5'
branch_labels = None
depends_on = None


def upgrade():
    pass
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column('event', sa.Column('Total_charge', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    pass
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_column('event', 'Total_charge')
    # ### end Alembic commands ###
