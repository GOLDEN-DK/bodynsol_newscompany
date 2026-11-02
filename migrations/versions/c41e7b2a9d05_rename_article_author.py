# 기존 기사의 작성자 표기를 바디앤솔매거진에서 ALL바른매거진으로 바꾸는 데이터 마이그레이션.
"""Rename article author to ALL바른매거진

Revision ID: c41e7b2a9d05
Revises: 8a3f17c9b2d1
Create Date: 2026-11-03

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c41e7b2a9d05'
down_revision = '8a3f17c9b2d1'
branch_labels = None
depends_on = None

OLD_AUTHOR = '바디앤솔매거진'
NEW_AUTHOR = 'ALL바른매거진'

article = sa.table('article', sa.column('author', sa.String))


def upgrade():
    op.execute(
        article.update()
        .where(article.c.author == OLD_AUTHOR)
        .values(author=NEW_AUTHOR)
    )


def downgrade():
    # 이 마이그레이션 이후 새로 작성된 기사(작성자 ALL바른매거진)도 함께 되돌아간다.
    op.execute(
        article.update()
        .where(article.c.author == NEW_AUTHOR)
        .values(author=OLD_AUTHOR)
    )
