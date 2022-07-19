"""All Tables created

Revision ID: 37d4f43b46fd
Revises: 5c73978f5cc5
Create Date: 2022-07-15 11:00:00.221070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37d4f43b46fd'
down_revision = '5c73978f5cc5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event_category')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event_category',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='event_category_pkey')
    )
    # ### end Alembic commands ###