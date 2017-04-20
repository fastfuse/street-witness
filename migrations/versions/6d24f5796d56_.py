"""empty message

Revision ID: 6d24f5796d56
Revises: 
Create Date: 2017-04-20 21:31:59.397299

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6d24f5796d56'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('incidents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Unicode(), nullable=True),
    sa.Column('description', sa.Unicode(), nullable=True),
    sa.Column('timestamp', sa.Date(), nullable=True),
    sa.Column('location', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('status', sa.Unicode(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('incidents')
    # ### end Alembic commands ###