"""fix

Revision ID: 2f3cb26931ac
Revises: 
Create Date: 2022-06-15 15:55:53.263395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f3cb26931ac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=250), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('price', sa.Float(precision=9, asdecimal=2), nullable=True),
    sa.Column('main_pic', sa.String(), nullable=True),
    sa.Column('pictures', sa.String(), nullable=True),
    sa.Column('is_automatic', sa.Boolean(), nullable=False),
    sa.Column('is_available', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('journal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('auto_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('time_start', sa.String(), nullable=True),
    sa.Column('time_end', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['auto_id'], ['auto.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('journal')
    op.drop_table('user')
    op.drop_table('auto')
    # ### end Alembic commands ###