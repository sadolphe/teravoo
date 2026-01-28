from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class PriceTierTemplate(Base):
    """
    Template de paliers tarifaires réutilisable par un producteur.
    Permet d'appliquer la même grille de réductions à plusieurs produits.
    """
    __tablename__ = "price_tier_templates"

    id = Column(Integer, primary_key=True, index=True)
    producer_id = Column(Integer, ForeignKey("producer_profiles.id"), nullable=False)

    name = Column(String, nullable=False)  # Ex: "Paliers Premium"
    description = Column(String, nullable=True)  # Ex: "Pour mes gros clients"
    is_default = Column(Boolean, default=False)  # Template par défaut du producteur

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    producer = relationship("ProducerProfile", back_populates="price_templates")
    tiers = relationship("TemplateTier", back_populates="template", cascade="all, delete-orphan", order_by="TemplateTier.position")
    products = relationship("Product", back_populates="price_template")


class TemplateTier(Base):
    """
    Palier d'un template - définit une réduction en pourcentage.
    Le prix final = prix_fob_produit * (1 - discount_percent/100)
    """
    __tablename__ = "template_tiers"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("price_tier_templates.id", ondelete="CASCADE"), nullable=False)

    min_quantity_kg = Column(Float, nullable=False)  # Quantité minimum du palier
    max_quantity_kg = Column(Float, nullable=True)   # Quantité max (null = illimité)
    discount_percent = Column(Float, nullable=False, default=0)  # Réduction vs prix de base (0 pour le premier palier)
    position = Column(Integer, nullable=False, default=0)  # Ordre d'affichage

    # Relationships
    template = relationship("PriceTierTemplate", back_populates="tiers")


class PriceTier(Base):
    """
    Palier tarifaire personnalisé pour un produit spécifique.
    Utilisé quand pricing_mode = "TIERED" (Option A)
    """
    __tablename__ = "price_tiers"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)

    min_quantity_kg = Column(Float, nullable=False)  # Quantité minimum du palier
    max_quantity_kg = Column(Float, nullable=True)   # Quantité max (null = illimité)
    price_per_kg = Column(Float, nullable=False)     # Prix FOB pour ce palier
    position = Column(Integer, nullable=False, default=0)  # Ordre d'affichage

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    product = relationship("Product", back_populates="price_tiers")


class PriceTierHistory(Base):
    """
    Historique des changements de prix d'un produit.
    Permet d'afficher "Prix en baisse de -X% depuis..."
    """
    __tablename__ = "price_tier_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)

    # Snapshot des données au moment du changement
    pricing_mode = Column(String, nullable=False)  # SINGLE, TIERED, TEMPLATE
    base_price_fob = Column(Float, nullable=False)  # Prix de base à cette date
    tiers_snapshot = Column(JSON, nullable=True)    # Copie des paliers [{min_qty, max_qty, price_per_kg}, ...]
    template_id_snapshot = Column(Integer, nullable=True)  # ID du template utilisé (si applicable)

    change_reason = Column(String, nullable=True)   # Ex: "Ajustement saisonnier", "Promotion"
    changed_at = Column(DateTime(timezone=True), server_default=func.now())
    changed_by = Column(String, nullable=True)      # User ID ou "System"

    # Relationships
    product = relationship("Product", back_populates="price_history")
