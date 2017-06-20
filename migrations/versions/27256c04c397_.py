"""empty message

Revision ID: 27256c04c397
Revises: 4cb2c73770a2
Create Date: 2017-06-20 22:00:53.218861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27256c04c397'
down_revision = '4cb2c73770a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(length=200), nullable=True),
    sa.Column('uploaded_on', sa.DateTime(), nullable=True),
    sa.Column('incident_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['incident_id'], ['incidents.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('files')
    # ### end Alembic commands ###
