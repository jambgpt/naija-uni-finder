"""Add feedback to admin dashboard.

Revision ID: 35a5c8ab3a14
Revises: d27c2d71dbca
Create Date: 2024-10-14 08:26:36.207902

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "35a5c8ab3a14"
down_revision = "d27c2d71dbca"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("feedback", schema=None) as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_feedback_user_id_user",  # Explicit constraint name
            "user",
            ["user_id"],
            ["id"],
        )

    with op.batch_alter_table("vote", schema=None) as batch_op:
        batch_op.create_unique_constraint("user_comment_uc", ["user_id", "comment_id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("vote", schema=None) as batch_op:
        batch_op.drop_constraint("user_comment_uc", type_="unique")

    with op.batch_alter_table("feedback", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_feedback_user_id_user", type_="foreignkey"
        )  # Explicit constraint name
        batch_op.drop_column("user_id")

    # ### end Alembic commands ###