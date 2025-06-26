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
    path: str = Field(..., description="Ruta del directorio a crear", example="documentos/trabajo")


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