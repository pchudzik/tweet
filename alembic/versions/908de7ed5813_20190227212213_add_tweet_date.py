"""add tweet date

Revision ID: 908de7ed5813
Revises: f7279b23c7d7
Create Date: 2019-02-27 21:22:13.656793

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '908de7ed5813'
down_revision = 'f7279b23c7d7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "tweets",
        sa.Column("post_time", sa.types.DateTime, nullable=False))


def downgrade():
    op.drop_column("tweets", "post_time")
