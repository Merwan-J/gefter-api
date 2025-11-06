"""update balances to two columns

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2025-11-06 11:10:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b2c3d4e5f6a7"
down_revision: Union[str, Sequence[str], None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Check if columns exist before adding/dropping
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col["name"] for col in inspector.get_columns("balances")]
    
    # Add new columns if they don't exist
    if "owed_to_user" not in columns:
        op.add_column("balances", sa.Column("owed_to_user", sa.Numeric(precision=10, scale=2), nullable=False, server_default="0"))
    if "user_owes" not in columns:
        op.add_column("balances", sa.Column("user_owes", sa.Numeric(precision=10, scale=2), nullable=False, server_default="0"))
    
    # Drop old balance column if it exists
    if "balance" in columns:
        op.drop_column("balances", "balance")


def downgrade() -> None:
    """Downgrade schema."""
    # Add back old balance column
    op.add_column("balances", sa.Column("balance", sa.Numeric(precision=10, scale=2), nullable=False, server_default="0"))
    
    # Drop new columns
    op.drop_column("balances", "owed_to_user")
    op.drop_column("balances", "user_owes")

