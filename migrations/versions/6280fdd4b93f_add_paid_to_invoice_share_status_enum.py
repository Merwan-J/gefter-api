"""add_paid_to_invoice_share_status_enum

Revision ID: 6280fdd4b93f
Revises: dee538493a4d
Create Date: 2025-11-07 11:15:33.373320

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '6280fdd4b93f'
down_revision: Union[str, Sequence[str], None] = 'dee538493a4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add PAID value to invoicesharestatus enum
    # Note: ALTER TYPE ... ADD VALUE cannot be run inside a transaction block in PostgreSQL
    # We need to execute this outside the transaction context
    op.execute("ALTER TYPE invoicesharestatus ADD VALUE IF NOT EXISTS 'PAID'")


def downgrade() -> None:
    """Downgrade schema."""
    # Note: PostgreSQL does not support removing enum values directly
    # This would require recreating the enum type, which is complex
    # For now, we'll leave it as a no-op
    pass
