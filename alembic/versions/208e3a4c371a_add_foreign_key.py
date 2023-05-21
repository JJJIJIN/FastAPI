"""add foreign key

Revision ID: 208e3a4c371a
Revises: 0ef8d1c9eb1b
Create Date: 2023-05-21 11:35:56.531341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '208e3a4c371a'
down_revision = '0ef8d1c9eb1b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key("post_user_fk",source_table="posts",referent_table="Users",
                          local_cols=["owner_id"],
                          remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_user_fk",table_name="posts")
    op.drop_column("posts","owner_id")
    pass
