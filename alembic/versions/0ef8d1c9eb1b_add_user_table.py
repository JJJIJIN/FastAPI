"""add user table

Revision ID: 0ef8d1c9eb1b
Revises: 17c7e577e440
Create Date: 2023-05-21 11:11:04.775977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ef8d1c9eb1b'
down_revision = '17c7e577e440'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("Users",
                    sa.Column("id",sa.Integer(),nullable=False,primary_key=True),
                    sa.Column("email",sa.String(),nullable=False,unique=True),
                    sa.Column("password",sa.String(),nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"),nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table("Users")
    pass
