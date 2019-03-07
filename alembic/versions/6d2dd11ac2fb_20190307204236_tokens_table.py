"""tokens table

Revision ID: 6d2dd11ac2fb
Revises: 908de7ed5813
Create Date: 2019-03-07 20:42:36.328479

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d2dd11ac2fb'
down_revision = '908de7ed5813'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'jwt_revoked_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('jti', sa.String(120), nullable=False, index=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('jwt_revoked_tokens')
