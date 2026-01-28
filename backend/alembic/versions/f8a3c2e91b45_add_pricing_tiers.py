"""Add pricing tiers tables

Revision ID: f8a3c2e91b45
Revises: d2a6e1944df1
Create Date: 2026-01-28 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8a3c2e91b45'
down_revision: Union[str, None] = 'd2a6e1944df1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # === CREATE NEW TABLES ===

    # Table: price_tier_templates (Templates de paliers réutilisables)
    op.create_table(
        'price_tier_templates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('producer_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('is_default', sa.Boolean(), nullable=True, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['producer_id'], ['producer_profiles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_price_tier_templates_id'), 'price_tier_templates', ['id'], unique=False)

    # Table: template_tiers (Paliers d'un template - en pourcentage)
    op.create_table(
        'template_tiers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('template_id', sa.Integer(), nullable=False),
        sa.Column('min_quantity_kg', sa.Float(), nullable=False),
        sa.Column('max_quantity_kg', sa.Float(), nullable=True),
        sa.Column('discount_percent', sa.Float(), nullable=False, default=0),
        sa.Column('position', sa.Integer(), nullable=False, default=0),
        sa.ForeignKeyConstraint(['template_id'], ['price_tier_templates.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_template_tiers_id'), 'template_tiers', ['id'], unique=False)

    # Table: price_tiers (Paliers personnalisés par produit)
    op.create_table(
        'price_tiers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('min_quantity_kg', sa.Float(), nullable=False),
        sa.Column('max_quantity_kg', sa.Float(), nullable=True),
        sa.Column('price_per_kg', sa.Float(), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False, default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_price_tiers_id'), 'price_tiers', ['id'], unique=False)

    # Table: price_tier_history (Historique des changements de prix)
    op.create_table(
        'price_tier_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('pricing_mode', sa.String(), nullable=False),
        sa.Column('base_price_fob', sa.Float(), nullable=False),
        sa.Column('tiers_snapshot', sa.JSON(), nullable=True),
        sa.Column('template_id_snapshot', sa.Integer(), nullable=True),
        sa.Column('change_reason', sa.String(), nullable=True),
        sa.Column('changed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('changed_by', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_price_tier_history_id'), 'price_tier_history', ['id'], unique=False)

    # === ADD COLUMNS TO PRODUCT TABLE ===
    op.add_column('product', sa.Column('moq_kg', sa.Float(), nullable=True, default=1.0))
    op.add_column('product', sa.Column('pricing_mode', sa.String(), nullable=True, default='SINGLE'))
    op.add_column('product', sa.Column('template_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_product_template', 'product', 'price_tier_templates', ['template_id'], ['id'])

    # Set default values for existing products
    op.execute("UPDATE product SET moq_kg = 1.0 WHERE moq_kg IS NULL")
    op.execute("UPDATE product SET pricing_mode = 'SINGLE' WHERE pricing_mode IS NULL")


def downgrade() -> None:
    # === REMOVE COLUMNS FROM PRODUCT TABLE ===
    op.drop_constraint('fk_product_template', 'product', type_='foreignkey')
    op.drop_column('product', 'template_id')
    op.drop_column('product', 'pricing_mode')
    op.drop_column('product', 'moq_kg')

    # === DROP TABLES ===
    op.drop_index(op.f('ix_price_tier_history_id'), table_name='price_tier_history')
    op.drop_table('price_tier_history')

    op.drop_index(op.f('ix_price_tiers_id'), table_name='price_tiers')
    op.drop_table('price_tiers')

    op.drop_index(op.f('ix_template_tiers_id'), table_name='template_tiers')
    op.drop_table('template_tiers')

    op.drop_index(op.f('ix_price_tier_templates_id'), table_name='price_tier_templates')
    op.drop_table('price_tier_templates')
