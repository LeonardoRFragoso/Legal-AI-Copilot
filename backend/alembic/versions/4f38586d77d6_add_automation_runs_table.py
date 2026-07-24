"""add automation_runs table

Revision ID: 4f38586d77d6
Revises: 
Create Date: 2026-07-24 14:54:50.002055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f38586d77d6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('automation_runs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('document_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('automation_type', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('current_step', sa.String(), nullable=False),
        sa.Column('progress_percent', sa.Integer(), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('summary_result', sa.JSON(), nullable=True),
        sa.Column('risk_result', sa.JSON(), nullable=True),
        sa.Column('webhook_status', sa.String(), nullable=False),
        sa.Column('webhook_error', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_automation_runs_document_id'), 'automation_runs', ['document_id'], unique=False)
    op.create_index(op.f('ix_automation_runs_status'), 'automation_runs', ['status'], unique=False)
    op.create_index(op.f('ix_automation_runs_user_id'), 'automation_runs', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_automation_runs_user_id'), table_name='automation_runs')
    op.drop_index(op.f('ix_automation_runs_status'), table_name='automation_runs')
    op.drop_index(op.f('ix_automation_runs_document_id'), table_name='automation_runs')
    op.drop_table('automation_runs')
