"""empty message

Revision ID: 5a405b70a06b
Revises: cb3e569e878f
Create Date: 2021-04-25 19:39:52.232026

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5a405b70a06b"
down_revision = "cb3e569e878f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("user_type", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "user_type")
    # ### end Alembic commands ###
