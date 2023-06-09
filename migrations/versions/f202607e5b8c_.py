"""empty message

Revision ID: f202607e5b8c
Revises: 6d5ac2c3105e
Create Date: 2023-06-14 21:50:49.962743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f202607e5b8c'
down_revision = '6d5ac2c3105e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('user_type', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'user_type')
    # ### end Alembic commands ###
