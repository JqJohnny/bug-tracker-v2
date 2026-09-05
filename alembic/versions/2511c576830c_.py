"""empty message

Revision ID: 2511c576830c
Revises: 73087c42f8ec
Create Date: 2026-09-04 23:46:07.808495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2511c576830c'
down_revision: Union[str, Sequence[str], None] = '73087c42f8ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
