"""user roli o'zgartirildi

Revision ID: d2693e153c39
Revises: 9f566088897e
Create Date: 2026-07-06 09:54:49.392678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2693e153c39'
down_revision: Union[str, Sequence[str], None] = '9f566088897e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Avval bazada yangi ENUM tipini yaratib olamiz
    role_enum = sa.Enum('FREELANCER', 'ADMIN', 'EMPLOYER', name='role')
    role_enum.create(op.get_bind(), checkfirst=True)

    # 2. Ustun tipini o'zgartiramiz (VARCHAR -> ENUM) va yangi server_default o'rnatamiz
    op.alter_column('users', 'role',
               existing_type=sa.VARCHAR(length=10),
               type_=role_enum,
               existing_nullable=False,
               postgresql_using="role::role", # Agar eski ma'lumotlar bo'lsa, ENUMga o'girish uchun
               server_default='FREELANCER')   # Bazaning o'zidagi default qiymat


def downgrade() -> None:
    # 1. Orqaga qaytarganda default qiymatni o'chiramiz va tipni yana VARCHAR qilamiz
    op.alter_column('users', 'role',
               existing_type=sa.Enum('FREELANCER', 'ADMIN', 'EMPLOYER', name='role'),
               type_=sa.VARCHAR(length=10),
               existing_nullable=False,
               server_default=None)

    # 2. Yaratilgan ENUM tipini bazadan butunlay o'chirib tashlaymiz
    sa.Enum(name='role').drop(op.get_bind(), checkfirst=True)