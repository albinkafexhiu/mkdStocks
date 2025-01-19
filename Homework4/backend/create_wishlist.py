from app.db.database import engine
from sqlalchemy import Column, Integer, String
from app.db.database import Base

# Define the WishlistItem model
class WishlistItem(Base):
    __tablename__ = "wishlist"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, nullable=False)

def init_wishlist_table():
    Base.metadata.create_all(bind=engine)
    print("Wishlist table created successfully!")

if __name__ == "__main__":
    init_wishlist_table()