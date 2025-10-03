# backend/app/models.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    iterations = relationship("DesignIteration", back_populates="owner")

class DesignIteration(Base):
    __tablename__ = "design_iterations"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String, index=True)
    sketch_url = Column(String)
    generated_image_url = Column(String, nullable=True)
    narrative = Column(Text, nullable=True)
    compliance_check = Column(Text, nullable=True)
    status = Column(String, default="processing")
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="iterations")