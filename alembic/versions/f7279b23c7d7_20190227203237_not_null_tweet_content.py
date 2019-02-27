"""not null tweet content

Revision ID: f7279b23c7d7
Revises: 36b535fa2cec
Create Date: 2019-02-27 20:32:37.675650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7279b23c7d7'
down_revision = '36b535fa2cec'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("tweets", "content", nullable=False)


def downgrade():
    op.alter_column("tweets", "content", nullable=True)
