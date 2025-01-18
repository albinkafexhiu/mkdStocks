from sqlalchemy import Column, Integer, String, Float, DateTime
from app.db.database import Base

class NewsItem(Base):
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    symbol = Column(String, nullable=True)  
    sentiment_score = Column(Float, nullable=True)
    recommendation = Column(String, nullable=True)