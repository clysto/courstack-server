"""empty message

Revision ID: 767e9fb8ca9c
Revises: bd8601be1589
Create Date: 2021-04-27 13:56:41.918640

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "767e9fb8ca9c"
down_revision = "bd8601be1589"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "course",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("teacher_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["teacher_id"],
            ["teacher.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("course")
    # ### end Alembic commands ###
