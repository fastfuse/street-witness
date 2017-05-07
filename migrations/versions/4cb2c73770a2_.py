"""empty message

Revision ID: 4cb2c73770a2
Revises: 6410e86ae882
Create Date: 2017-05-01 16:27:47.542177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4cb2c73770a2'
down_revision = '6410e86ae882'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('incidents', sa.Column('reporter', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'incidents', 'users', ['reporter'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'incidents', type_='foreignkey')
    op.drop_column('incidents', 'reporter')
    # ### end Alembic commands ###
