# -*- coding: utf-8 -*-
"""
Modelo Client
============

Modelo SQLAlchemy para la tabla de clientes.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class Client(Base):
    """
    Modelo para la tabla de clientes.
    
    Attributes:
        id (int): ID único del cliente
        name (str): Nombre del cliente
        email (str): Email del cliente
        phone (str): Teléfono del cliente
        address (str): Dirección del cliente
        notes (str): Notas adicionales
        is_active (bool): Si el cliente está activo
        created_at (datetime): Fecha de creación
        updated_at (datetime): Fecha de última actualización
    """
    
    __tablename__ = "clients"
    
    # Campos principales
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Campos de auditoría
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relaciones
    documents = relationship("Document", back_populates="client")
    
    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.name}', email='{self.email}')>"
    
    def to_dict(self):
        """
        Convierte el cliente a un diccionario.
        
        Returns:
            dict: Diccionario con los datos del cliente
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "notes": self.notes,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        } 