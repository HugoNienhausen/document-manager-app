# -*- coding: utf-8 -*-
"""
Modelos de datos
================

Este módulo contiene los modelos Pydantic para validación de datos
y estructuración de respuestas de la API.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class DirectoryCreate(BaseModel):
    """
    Modelo para crear un directorio.
    
    Attributes:
        path (str): Ruta del directorio a crear
    """
    path: str = Field(..., description="Ruta del directorio a crear")


class DirectoryResponse(BaseModel):
    """
    Modelo de respuesta para operaciones con directorios.
    
    Attributes:
        message (str): Mensaje de confirmación
        path (str): Ruta del directorio
        created_at (datetime): Fecha de creación
    """
    message: str = Field(..., description="Mensaje de confirmación")
    path: str = Field(..., description="Ruta del directorio")
    created_at: datetime = Field(default_factory=datetime.now, description="Fecha de creación")


class FileUploadResponse(BaseModel):
    """
    Modelo de respuesta para subida de archivos.
    
    Attributes:
        message (str): Mensaje de confirmación
        filename (str): Nombre del archivo subido
        path (str): Ruta donde se guardó el archivo
        size (int): Tamaño del archivo en bytes
        uploaded_at (datetime): Fecha de subida
    """
    message: str = Field(..., description="Mensaje de confirmación")
    filename: str = Field(..., description="Nombre del archivo subido")
    path: str = Field(..., description="Ruta donde se guardó el archivo")
    size: int = Field(..., description="Tamaño del archivo en bytes")
    uploaded_at: datetime = Field(default_factory=datetime.now, description="Fecha de subida")


class DirectoryInfo(BaseModel):
    """
    Modelo para información de directorios.
    
    Attributes:
        name (str): Nombre del directorio
        path (str): Ruta completa del directorio
        files_count (int): Número de archivos en el directorio
        created_at (datetime): Fecha de creación del directorio
    """
    name: str = Field(..., description="Nombre del directorio")
    path: str = Field(..., description="Ruta completa del directorio")
    files_count: int = Field(..., description="Número de archivos en el directorio")
    created_at: datetime = Field(..., description="Fecha de creación del directorio")


class FileInfo(BaseModel):
    """
    Modelo para información de archivos.
    
    Attributes:
        name (str): Nombre del archivo
        path (str): Ruta completa del archivo
        size (int): Tamaño del archivo en bytes
        extension (str): Extensión del archivo
        modified_at (datetime): Fecha de última modificación
    """
    name: str = Field(..., description="Nombre del archivo")
    path: str = Field(..., description="Ruta completa del archivo")
    size: int = Field(..., description="Tamaño del archivo en bytes")
    extension: str = Field(..., description="Extensión del archivo")
    modified_at: datetime = Field(..., description="Fecha de última modificación")


class ErrorResponse(BaseModel):
    """
    Modelo para respuestas de error.
    
    Attributes:
        error (str): Mensaje de error
        detail (Optional[str]): Detalles adicionales del error
        timestamp (datetime): Fecha y hora del error
    """
    error: str = Field(..., description="Mensaje de error")
    detail: Optional[str] = Field(None, description="Detalles adicionales del error")
    timestamp: datetime = Field(default_factory=datetime.now, description="Fecha y hora del error")


class HealthCheck(BaseModel):
    """
    Modelo para verificación de salud de la aplicación.
    
    Attributes:
        status (str): Estado de la aplicación
        version (str): Versión de la aplicación
        uptime (float): Tiempo de actividad en segundos
        timestamp (datetime): Fecha y hora de la verificación
    """
    status: str = Field(..., description="Estado de la aplicación")
    version: str = Field(..., description="Versión de la aplicación")
    uptime: float = Field(..., description="Tiempo de actividad en segundos")
    timestamp: datetime = Field(default_factory=datetime.now, description="Fecha y hora de la verificación")


# ============================================================================
# MODELOS PARA DOCUMENTOS CON METADATOS
# ============================================================================

class DocumentMetadata(BaseModel):
    """
    Modelo para metadatos de documentos.
    
    Attributes:
        document_type_id (int): ID del tipo de documento
        client_id (Optional[int]): ID del cliente (opcional)
        category_id (int): ID de la categoría
        upload_date (Optional[datetime]): Fecha de subida (automática si no se especifica)
    """
    document_type_id: int = Field(..., description="ID del tipo de documento")
    client_id: Optional[int] = Field(None, description="ID del cliente (opcional)")
    category_id: int = Field(..., description="ID de la categoría")
    upload_date: Optional[datetime] = Field(None, description="Fecha de subida")


class DocumentUploadRequest(BaseModel):
    """
    Modelo para solicitud de subida de documento con metadatos.
    
    Attributes:
        file (UploadFile): Archivo a subir
        path (str): Ruta del directorio destino
        metadata (DocumentMetadata): Metadatos del documento
    """
    path: str = Field(..., description="Ruta del directorio destino")
    metadata: DocumentMetadata = Field(..., description="Metadatos del documento")


class DocumentResponse(BaseModel):
    """
    Modelo de respuesta para documentos.
    
    Attributes:
        id (int): ID del documento
        filename (str): Nombre del archivo
        file_hash (str): Hash del archivo
        document_type (str): Tipo de documento
        client (Optional[str]): Cliente (si aplica)
        category (str): Categoría
        local_path (str): Ruta local del archivo
        file_size (int): Tamaño del archivo
        upload_date (datetime): Fecha de subida
        created_at (datetime): Fecha de creación del registro
    """
    id: int = Field(..., description="ID del documento")
    filename: str = Field(..., description="Nombre del archivo")
    file_hash: str = Field(..., description="Hash del archivo")
    document_type: str = Field(..., description="Tipo de documento")
    client: Optional[str] = Field(None, description="Cliente (si aplica)")
    category: str = Field(..., description="Categoría")
    local_path: str = Field(..., description="Ruta local del archivo")
    file_size: int = Field(..., description="Tamaño del archivo")
    upload_date: datetime = Field(..., description="Fecha de subida")
    created_at: datetime = Field(..., description="Fecha de creación del registro")


class DocumentUploadResponse(BaseModel):
    """
    Modelo de respuesta para subida de documentos con metadatos.
    
    Attributes:
        message (str): Mensaje de confirmación
        document (DocumentResponse): Información del documento creado
        uploaded_at (datetime): Fecha de subida
    """
    message: str = Field(..., description="Mensaje de confirmación")
    document: DocumentResponse = Field(..., description="Información del documento creado")
    uploaded_at: datetime = Field(default_factory=datetime.now, description="Fecha de subida")


class DocumentTypeResponse(BaseModel):
    """
    Modelo de respuesta para tipos de documento.
    
    Attributes:
        id (int): ID del tipo de documento
        name (str): Nombre del tipo de documento
        description (Optional[str]): Descripción del tipo
    """
    id: int = Field(..., description="ID del tipo de documento")
    name: str = Field(..., description="Nombre del tipo de documento")
    description: Optional[str] = Field(None, description="Descripción del tipo")


class ClientResponse(BaseModel):
    """
    Modelo de respuesta para clientes.
    
    Attributes:
        id (int): ID del cliente
        name (str): Nombre del cliente
        email (Optional[str]): Email del cliente
        phone (Optional[str]): Teléfono del cliente
    """
    id: int = Field(..., description="ID del cliente")
    name: str = Field(..., description="Nombre del cliente")
    email: Optional[str] = Field(None, description="Email del cliente")
    phone: Optional[str] = Field(None, description="Teléfono del cliente")


class CategoryResponse(BaseModel):
    """
    Modelo de respuesta para categorías.
    
    Attributes:
        id (int): ID de la categoría
        name (str): Nombre de la categoría
        description (Optional[str]): Descripción de la categoría
    """
    id: int = Field(..., description="ID de la categoría")
    name: str = Field(..., description="Nombre de la categoría")
    description: Optional[str] = Field(None, description="Descripción de la categoría")


# ============================================================================
# MODELOS PARA OPERACIONES CRUD DE METADATOS
# ============================================================================

class DocumentTypeCreate(BaseModel):
    """
    Modelo para crear un tipo de documento.
    
    Attributes:
        name (str): Nombre del tipo de documento
        description (Optional[str]): Descripción del tipo
    """
    name: str = Field(..., description="Nombre del tipo de documento")
    description: Optional[str] = Field(None, description="Descripción del tipo")


class DocumentTypeUpdate(BaseModel):
    """
    Modelo para actualizar un tipo de documento.
    
    Attributes:
        name (Optional[str]): Nombre del tipo de documento
        description (Optional[str]): Descripción del tipo
    """
    name: Optional[str] = Field(None, description="Nombre del tipo de documento")
    description: Optional[str] = Field(None, description="Descripción del tipo")


class CategoryCreate(BaseModel):
    """
    Modelo para crear una categoría.
    
    Attributes:
        name (str): Nombre de la categoría
        description (Optional[str]): Descripción de la categoría
    """
    name: str = Field(..., description="Nombre de la categoría")
    description: Optional[str] = Field(None, description="Descripción de la categoría")


class CategoryUpdate(BaseModel):
    """
    Modelo para actualizar una categoría.
    
    Attributes:
        name (Optional[str]): Nombre de la categoría
        description (Optional[str]): Descripción de la categoría
    """
    name: Optional[str] = Field(None, description="Nombre de la categoría")
    description: Optional[str] = Field(None, description="Descripción de la categoría")


class ClientCreate(BaseModel):
    """
    Modelo para crear un cliente.
    
    Attributes:
        name (str): Nombre del cliente
        email (Optional[str]): Email del cliente
        phone (Optional[str]): Teléfono del cliente
    """
    name: str = Field(..., description="Nombre del cliente")
    email: Optional[str] = Field(None, description="Email del cliente")
    phone: Optional[str] = Field(None, description="Teléfono del cliente")


class ClientUpdate(BaseModel):
    """
    Modelo para actualizar un cliente.
    
    Attributes:
        name (Optional[str]): Nombre del cliente
        email (Optional[str]): Email del cliente
        phone (Optional[str]): Teléfono del cliente
    """
    name: Optional[str] = Field(None, description="Nombre del cliente")
    email: Optional[str] = Field(None, description="Email del cliente")
    phone: Optional[str] = Field(None, description="Teléfono del cliente") 