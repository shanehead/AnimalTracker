"""empty message

Revision ID: 106f583b8af8
Revises: 2b907bb4ddab
Create Date: 2015-03-08 18:13:25.921987

"""

# revision identifiers, used by Alembic.
revision = '106f583b8af8'
down_revision = '2b907bb4ddab'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('animals', sa.Column('avatar', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('animals', 'avatar')
    ### end Alembic commands ###
