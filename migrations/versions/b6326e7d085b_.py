"""empty message

Revision ID: b6326e7d085b
Revises: 749ecca4e90a
Create Date: 2022-06-17 15:29:05.838629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6326e7d085b'
down_revision = '749ecca4e90a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('venue_type', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'venue_type')
    # ### end Alembic commands ###
