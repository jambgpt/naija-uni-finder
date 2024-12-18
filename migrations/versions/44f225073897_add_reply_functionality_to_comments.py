"""Add reply functionality to comments

Revision ID: 44f225073897
Revises: initial_migration_2024
Create Date: 2024-11-01 17:31:19.309662

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '44f225073897'
down_revision = 'initial_migration_2024'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # First, add unique constraint to university table
    with op.batch_alter_table('university', schema=None) as batch_op:
        batch_op.create_index('idx_university_name', ['university_name'], unique=False)
        batch_op.create_unique_constraint('uq_university_name', ['university_name'])

    # Then modify course table since it depends on university's unique constraint
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.create_index('idx_course_name', ['course_name'], unique=False)
        batch_op.create_index('idx_course_university', ['university_name'], unique=False)
        batch_op.create_foreign_key('fk_course_university', 'university', ['university_name'], ['university_name'])
        batch_op.drop_column('abbrv')

    # Finally add comment reply functionality
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parent_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_comment_parent', 'comment', ['parent_id'], ['id'], ondelete='CASCADE')

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint('fk_comment_parent', type_='foreignkey')
        batch_op.drop_column('parent_id')

    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.add_column(sa.Column('abbrv', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.drop_constraint('fk_course_university', type_='foreignkey')
        batch_op.drop_index('idx_course_university')
        batch_op.drop_index('idx_course_name')

    with op.batch_alter_table('university', schema=None) as batch_op:
        batch_op.drop_constraint('uq_university_name', type_='unique')
        batch_op.drop_index('idx_university_name')