"""migration

Revision ID: a11e771c1ce4
Revises: 0000282a2c33
Create Date: 2024-08-30 00:52:56.263174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'a11e771c1ce4'
down_revision: Union[str, None] = '0000282a2c33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('payments', 'status',
               existing_type=mysql.ENUM('cash', 'mpesa'),
               type_=sa.Enum('Completed', 'Pending', name='paymentstatusenum'),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('payments', 'status',
               existing_type=sa.Enum('Completed', 'Pending', name='paymentstatusenum'),
               type_=mysql.ENUM('cash', 'mpesa'),
               existing_nullable=False)
    # ### end Alembic commands ###
