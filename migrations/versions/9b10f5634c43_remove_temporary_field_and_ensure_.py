"""Remove temporary field and ensure created_at

Revision ID: 9b10f5634c43
Revises: 9ec24f93d444
Create Date: 2024-05-15 16:26:33.843543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b10f5634c43'
down_revision = '9ec24f93d444'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('temp_field')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('temp_field', sa.VARCHAR(length=10), nullable=True))

    # ### end Alembic commands ###
