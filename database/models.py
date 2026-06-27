from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     first_name: Mapped[str] = Column(String)
#     last_name: Mapped[str] = Column(String)
#     user_age: Mapped[int] = Column(Integer)
#     user_mail: Mapped[str] = Column(String, unique=True)
#     created_at: Mapped[DateTime] = Column(DateTime, server_default=func.now())
#     updated_at: Mapped[DateTime] = Column(DateTime, server_default=func.now(), onupdate=func.now())

#     devices = relationship("Device", back_populates="user")


