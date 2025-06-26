# -*- coding: utf-8 -*-
"""
Modelo Category
==============

Modelo SQLAlchemy para la tabla de categorías.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class Category(Base):
    """
    Modelo para la tabla de categorías.
    
    Attributes:
        id (int): ID único de la categoría
        name (str): Nombre de la categoría
        description (str): Descripción de la categoría
        color (str): Color para identificar la categoría
        is_active (bool): Si la categoría está activa
        created_at (datetime): Fecha de creación
        updated_at (datetime): Fecha de última actualización
    """
    
    __tablename__ = "categories"
    
    # Campos principales
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    color = Column(String(7), nullable=True, default="#3b82f6")  # Color hex
    
    # Campos de auditoría
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relaciones
    documents = relationship("Document", back_populates="category")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', color='{self.color}')>"
    
    def to_dict(self):
        """
        Convierte la categoría a un diccionario.
        
        Returns:
            dict: Diccionario con los datos de la categoría
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "color": self.color,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        } 