# -*- coding: utf-8 -*-
"""
Modelo DocumentType
==================

Modelo SQLAlchemy para la tabla de tipos de documentos.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class DocumentType(Base):
    """
    Modelo para la tabla de tipos de documentos.
    
    Attributes:
        id (int): ID único del tipo de documento
        name (str): Nombre del tipo de documento
        description (str): Descripción del tipo de documento
        icon (str): Icono para representar el tipo
        is_active (bool): Si el tipo está activo
        created_at (datetime): Fecha de creación
        updated_at (datetime): Fecha de última actualización
    """
    
    __tablename__ = "document_types"
    
    # Campos principales
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True, default="fas fa-file-pdf")
    
    # Campos de auditoría
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relaciones
    documents = relationship("Document", back_populates="document_type")
    
    def __repr__(self):
        return f"<DocumentType(id={self.id}, name='{self.name}', icon='{self.icon}')>"
    
    def to_dict(self):
        """
        Convierte el tipo de documento a un diccionario.
        
        Returns:
            dict: Diccionario con los datos del tipo de documento
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        } 