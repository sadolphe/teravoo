from app.db.base_class import Base

# Import models to ensure they are registered with Base
# This is critical for Alembic to detect them
from app.models.sourcing import SourcingRequest, SourcingOffer
from app.models.product import Product
from app.models.order import Order
from app.models.producer import ProducerProfile, TraceabilityEvent
from app.models.user import User
