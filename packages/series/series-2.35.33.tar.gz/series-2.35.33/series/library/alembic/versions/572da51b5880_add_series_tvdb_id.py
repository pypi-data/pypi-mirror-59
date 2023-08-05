"""add Series.tvdb_id

Revision ID: 572da51b5880
Revises: 016150597609
Create Date: 2019-02-16 13:28:02.033632

"""

# revision identifiers, used by Alembic.
revision = '572da51b5880'
down_revision = '016150597609'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('series', sa.Column('tvdb_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    pass
