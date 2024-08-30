"""migration

Revision ID: 1ee05e6b7bd7
Revises: a11e771c1ce4
Create Date: 2024-08-30 14:21:26.742050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '1ee05e6b7bd7'
down_revision: Union[str, None] = 'a11e771c1ce4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('checkout_req_id', sa.String(length=100), nullable=True))
    op.add_column('transactions', sa.Column('response_code', sa.String(length=10), nullable=False))
    op.add_column('transactions', sa.Column('response_description', sa.String(length=255), nullable=False))
    op.add_column('transactions', sa.Column('customer_message', sa.String(length=255), nullable=False))
    op.alter_column('transactions', 'status',
               existing_type=mysql.VARCHAR(length=20),
               type_=sa.Enum('Completed', 'Pending', name='transactionstatusenum'),
               nullable=False)
    op.create_index(op.f('ix_transactions_checkout_req_id'), 'transactions', ['checkout_req_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transactions_checkout_req_id'), table_name='transactions')
    op.alter_column('transactions', 'status',
               existing_type=sa.Enum('Completed', 'Pending', name='transactionstatusenum'),
               type_=mysql.VARCHAR(length=20),
               nullable=True)
    op.drop_column('transactions', 'customer_message')
    op.drop_column('transactions', 'response_description')
    op.drop_column('transactions', 'response_code')
    op.drop_column('transactions', 'checkout_req_id')
    # ### end Alembic commands ###
