"""initial

Revision ID: 36b535fa2cec
Revises: 
Create Date: 2019-02-20 21:11:15.087685

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '36b535fa2cec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=True),
        sa.Column('password', sa.String(length=64), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table(
        'followers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('follower_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'tweets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content', sa.String(length=256), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('tweets')
    op.drop_table('followers')
    op.drop_table('users')
