"""Add collection status table

Revision ID: 5
Revises: 4
Create Date: 2023-01-26 08:30:05.524959

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision = '5'
down_revision = '4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('collection_status',
    sa.Column('repo_id', sa.BigInteger(), nullable=False),
    sa.Column('core_data_last_collected', postgresql.TIMESTAMP(), nullable=True),
    sa.Column('core_status', sa.String(), server_default=sa.text("'Pending'"), nullable=False),
    sa.Column('core_task_id', sa.String(), nullable=True),
    sa.Column('secondary_data_last_collected', postgresql.TIMESTAMP(), nullable=True),
    sa.Column('secondary_status', sa.String(), server_default=sa.text("'Pending'"), nullable=False),
    sa.Column('secondary_task_id', sa.String(), nullable=True),
    sa.Column('event_last_collected', postgresql.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['repo_id'], ['augur_data.repo.repo_id'], name='collection_status_repo_id_fk'),
    sa.PrimaryKeyConstraint('repo_id'),
    schema='augur_operations'
    )

    # add collection status for any existing repos
    conn = op.get_bind()
    repos = conn.execute(text("""SELECT repo_id from repo""")).fetchall()

    for repo in repos:
        repo_id = repo[0]
        conn.execute(text(f"""INSERT INTO "augur_operations"."collection_status" ("repo_id") VALUES ({repo_id});"""))

    conn.execute(text("""
        UPDATE augur_operations.config
        SET value = '600'
        WHERE section_name = 'Tasks'
        AND setting_name = 'collection_interval';
    """))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('collection_status', schema='augur_operations')
    # ### end Alembic commands ###
