"""added is_expired field

Revision ID: 57b640a350b4
Revises: 88fcb504cf51
Create Date: 2023-04-05 17:21:09.072010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57b640a350b4'
down_revision = '88fcb504cf51'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jobs', sa.Column('is_expired', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('jobs', 'is_expired')
    # ### end Alembic commands ###