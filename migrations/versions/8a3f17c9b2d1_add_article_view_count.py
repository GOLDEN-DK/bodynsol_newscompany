"""Add article view count

Revision ID: 8a3f17c9b2d1
Revises: 6fd9c81d1407
Create Date: 2026-08-20

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a3f17c9b2d1'
down_revision = '6fd9c81d1407'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.add_column(sa.Column(
            'view_count',
            sa.Integer(),
            server_default=sa.text('0'),
            nullable=False
        ))


def downgrade():
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.drop_column('view_count')
