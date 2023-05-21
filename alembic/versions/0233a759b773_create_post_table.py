"""create post table

Revision ID: 0233a759b773
Revises: 
Create Date: 2023-05-20 20:01:33.223973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0233a759b773'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable = False,primary_key = True),
                    sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
