from app.db.base import Base
from app.db.session import engine
# Import all models to ensure they are registered
from app.models.user import User

def init():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

if __name__ == "__main__":
    init()
