"""fix quiz table attributes

Revision ID: bc5b3ec5a9ca
Revises: 7242c70bf6d3
Create Date: 2025-03-02 23:22:39.338779

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision: str = "bc5b3ec5a9ca"
down_revision: Union[str, None] = "7242c70bf6d3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "quiz", sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=False)
    )
    op.add_column(
        "quiz",
        sa.Column(
            "quiz_type", sa.Enum("multiple", "single", name="quiztype"), nullable=True
        ),
    )
    op.add_column(
        "quiz",
        sa.Column("mode", sa.Enum("normal", "contest", name="quizmode"), nullable=True),
    )
    op.add_column("quiz", sa.Column("total_questions", sa.Integer(), nullable=False))
    op.add_column("quiz", sa.Column("total_likes", sa.Integer(), nullable=False))
    op.add_column("quiz", sa.Column("total_points", sa.Integer(), nullable=False))
    op.add_column("quiz", sa.Column("points_to_pass", sa.Integer(), nullable=False))
    op.add_column("quiz", sa.Column("time_limit", sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("quiz", "time_limit")
    op.drop_column("quiz", "points_to_pass")
    op.drop_column("quiz", "total_points")
    op.drop_column("quiz", "total_likes")
    op.drop_column("quiz", "total_questions")
    op.drop_column("quiz", "mode")
    op.drop_column("quiz", "quiz_type")
    op.drop_column("quiz", "title")
    # ### end Alembic commands ###
