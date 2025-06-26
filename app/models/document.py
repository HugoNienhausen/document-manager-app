# -*- coding: utf-8 -*-
"""
Modelo Document
==============

Modelo SQLAlchemy para la tabla de documentos.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import hashlib
import os

from ..database import Base


class Document(Base):
    """
    Modelo para la tabla de documentos.
    
    Attributes:
        id (int): ID único del documento
        filename (str): Nombre original del archivo
        file_hash (str): Hash único del archivo para evitar duplicados
        document_type_id (int): ID del tipo de documento
        client_id (int): ID del cliente (opcional)
        category_id (int): ID de la categoría
        local_path (str): Ruta local del archivo
        extracted_text (str): Texto extraído del PDF
        file_size (int): Tamaño del archivo en bytes
        upload_date (datetime): Fecha de subida
        is_active (bool): Si el documento está activo
        created_at (datetime): Fecha de creación del registro
        updated_at (datetime): Fecha de última actualización
    """
    
    __tablename__ = "documents"
    
    # Campos principales
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False, index=True)
    file_hash = Column(String(64), unique=True, nullable=False, index=True)
    document_type_id = Column(Integer, ForeignKey("document_types.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    local_path = Column(String(500), nullable=False)
    extracted_text = Column(Text, nullable=True)
    file_size = Column(Integer, nullable=False)
    
    # Campos de auditoría
    upload_date = Column(DateTime, default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relaciones
    document_type = relationship("DocumentType", back_populates="documents")
    client = relationship("Client", back_populates="documents")
    category = relationship("Category", back_populates="documents")
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename='{self.filename}', type='{self.document_type.name if self.document_type else 'N/A'}')>"
    
    @classmethod
    def generate_file_hash(cls, file_path: str) -> str:
        """
        Genera un hash SHA-256 del archivo.
        
        Args:
            file_path (str): Ruta del archivo
            
        Returns:
            str: Hash SHA-256 del archivo
        """
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    @classmethod
    def generate_file_hash_from_content(cls, content: bytes) -> str:
        """
        Genera un hash SHA-256 del contenido del archivo.
        
        Args:
            content (bytes): Contenido del archivo
            
        Returns:
            str: Hash SHA-256 del contenido
        """
        return hashlib.sha256(content).hexdigest()
    
    def get_file_size(self) -> int:
        """
        Obtiene el tamaño actual del archivo.
        
        Returns:
            int: Tamaño del archivo en bytes
        """
        if os.path.exists(self.local_path):
            return os.path.getsize(self.local_path)
        return 0
    
    def file_exists(self) -> bool:
        """
        Verifica si el archivo físico existe.
        
        Returns:
            bool: True si el archivo existe, False en caso contrario
        """
        return os.path.exists(self.local_path) 