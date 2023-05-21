"""add content to post table

Revision ID: 17c7e577e440
Revises: 0233a759b773
Create Date: 2023-05-21 10:53:16.816301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17c7e577e440'
down_revision = '0233a759b773'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("content",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
