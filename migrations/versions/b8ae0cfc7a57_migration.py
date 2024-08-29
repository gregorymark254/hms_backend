"""migration

Revision ID: b8ae0cfc7a57
Revises: a363691f54b8
Create Date: 2024-08-29 17:07:07.062166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'b8ae0cfc7a57'
down_revision: Union[str, None] = 'a363691f54b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transactions', 'id')
    op.drop_column('transactions', 'mpesa_ref')
    op.drop_column('transactions', 'phone_no')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('phone_no', mysql.VARCHAR(length=20), nullable=False))
    op.add_column('transactions', sa.Column('mpesa_ref', mysql.VARCHAR(length=100), nullable=True))
    op.add_column('transactions', sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False))
    # ### end Alembic commands ###
