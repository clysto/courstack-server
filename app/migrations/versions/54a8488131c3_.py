"""empty message

Revision ID: 54a8488131c3
Revises: 246db17ff3bc
Create Date: 2021-04-28 13:14:32.433581

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "54a8488131c3"
down_revision = "246db17ff3bc"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "course_section",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("content", sa.String(), nullable=True),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("attachments", sa.ARRAY(sa.String(), dimensions=10), nullable=True),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["course.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("course_section")
    # ### end Alembic commands ###
