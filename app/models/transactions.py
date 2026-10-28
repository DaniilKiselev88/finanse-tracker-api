from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.db import Base

class Transaction(Base):
    __tablename__ = "transactions"
    
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    type = Column(String(20), nullable=False)
    category = Column(String(50), nullable=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())