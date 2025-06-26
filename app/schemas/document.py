# -*- coding: utf-8 -*-
"""
Esquemas de Document
====================

Esquemas Pydantic para la gestión de documentos.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DocumentBase(BaseModel):
    """Esquema base para documentos."""
    filename: str = Field(..., description="Nombre del archivo")
    document_type_id: int = Field(..., description="ID del tipo de documento")
    client_id: Optional[int] = Field(None, description="ID del cliente (opcional)")
    category_id: int = Field(..., description="ID de la categoría")
    extracted_text: Optional[str] = Field(None, description="Texto extraído del PDF")


class DocumentCreate(DocumentBase):
    """Esquema para crear un documento."""
    file_hash: str = Field(..., description="Hash único del archivo")
    local_path: str = Field(..., description="Ruta local del archivo")
    file_size: int = Field(..., description="Tamaño del archivo en bytes")


class DocumentUpdate(BaseModel):
    """Esquema para actualizar un documento."""
    filename: Optional[str] = Field(None, description="Nombre del archivo")
    document_type_id: Optional[int] = Field(None, description="ID del tipo de documento")
    client_id: Optional[int] = Field(None, description="ID del cliente")
    category_id: Optional[int] = Field(None, description="ID de la categoría")
    extracted_text: Optional[str] = Field(None, description="Texto extraído del PDF")
    is_active: Optional[bool] = Field(None, description="Si el documento está activo")


class DocumentResponse(DocumentBase):
    """Esquema para respuesta de documento."""
    id: int
    file_hash: str
    local_path: str
    file_size: int
    upload_date: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    # Información de relaciones
    document_type_name: Optional[str] = None
    client_name: Optional[str] = None
    category_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class DocumentList(BaseModel):
    """Esquema para lista de documentos."""
    documents: List[DocumentResponse]
    total: int
    page: int
    per_page: int
    total_pages: int 