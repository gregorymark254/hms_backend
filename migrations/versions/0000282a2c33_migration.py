"""migration

Revision ID: 0000282a2c33
Revises: f3ded14731ff
Create Date: 2024-08-30 00:51:31.997229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '0000282a2c33'
down_revision: Union[str, None] = 'f3ded14731ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('payments', 'status',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.Enum('cash', 'mpesa', name='paymentenum'),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('payments', 'status',
               existing_type=sa.Enum('cash', 'mpesa', name='paymentenum'),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=False)
    # ### end Alembic commands ###
