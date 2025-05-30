"""empty message

Revision ID: 54348345d1a6
Revises: 30a78a22df97
Create Date: 2025-05-10 10:13:49.506563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54348345d1a6'
down_revision = '30a78a22df97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet_films',
    sa.Column('planet_id', sa.Integer(), nullable=False),
    sa.Column('film_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['film_id'], ['film.id'], ),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.PrimaryKeyConstraint('planet_id', 'film_id')
    )
    op.create_table('people_films',
    sa.Column('people_id', sa.Integer(), nullable=False),
    sa.Column('film_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['film_id'], ['film.id'], ),
    sa.ForeignKeyConstraint(['people_id'], ['people.id'], ),
    sa.PrimaryKeyConstraint('people_id', 'film_id')
    )
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planet_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'planet', ['planet_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('planet_id')

    op.drop_table('people_films')
    op.drop_table('planet_films')
    # ### end Alembic commands ###
