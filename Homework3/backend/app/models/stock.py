from sqlalchemy import Column, Integer, String
from app.db.database import Base

class WishlistItem(Base):
    __tablename__ = "wishlist"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, nullable=False)