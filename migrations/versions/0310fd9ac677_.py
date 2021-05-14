"""empty message

Revision ID: 0310fd9ac677
Revises: 84203a5d5ffd
Create Date: 2020-08-16 17:42:13.420286

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0310fd9ac677'
down_revision = '84203a5d5ffd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    """op.create_table('Subscribe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('sub', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['Client.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.drop_table('sqlite_sequence')
    op.drop_table('subscribe')
    with op.batch_alter_table('Client', schema=None) as batch_op:
        batch_op.alter_column('address',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('date_of_birth',
               existing_type=sa.NUMERIC(),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('first_name',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('gender',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('last_name',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('phone_number',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.create_unique_constraint(None, ['phone_number'])
        batch_op.create_unique_constraint(None, ['email'])
        batch_op.create_unique_constraint(None, ['id'])"""

    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.add_column(sa.Column('confirmed', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.drop_column('confirmed')

    """with op.batch_alter_table('Client', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('phone_number',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('last_name',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('gender',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('first_name',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('date_of_birth',
               existing_type=sa.NUMERIC(),
               nullable=False)
        batch_op.alter_column('address',
               existing_type=sa.TEXT(),
               nullable=False)

    op.create_table('subscribe',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('client_id', sa.INTEGER(), nullable=True),
    sa.Column('sub', sa.INTEGER(), nullable=True),
    sa.Column('start_date', sa.DATE(), nullable=True),
    sa.Column('end_date', sa.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['Client.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('sqlite_sequence',
    sa.Column('name', sa.NullType(), nullable=True),
    sa.Column('seq', sa.NullType(), nullable=True)
    )
    op.drop_table('Subscribe')"""
    # ### end Alembic commands ###