"""empty message

Revision ID: f84aa6163305
Revises: 00a4502a210a
Create Date: 2022-06-24 12:40:35.889176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f84aa6163305'
down_revision = '00a4502a210a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue_get_decorator', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue_get_decorator', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    # ### end Alembic commands ###
