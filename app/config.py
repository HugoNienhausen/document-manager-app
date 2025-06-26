# -*- coding: utf-8 -*-
"""
Configuración de la aplicación
==============================

Este módulo contiene todas las configuraciones centralizadas de la aplicación.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuraciones de la aplicación usando Pydantic.
    
    Permite cargar configuraciones desde variables de entorno
    o usar valores por defecto.
    """
    
    # Configuración del servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Configuración de archivos
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: list = [".pdf"]
    
    # Configuración de seguridad
    SECRET_KEY: str = "tu-clave-secreta-aqui-cambiala-en-produccion"
    
    # Configuración de logs
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()


def get_upload_path() -> Path:
    """
    Obtiene la ruta del directorio de uploads.
    
    Returns:
        Path: Ruta absoluta del directorio de uploads
        
    Raises:
        OSError: Si no se puede crear el directorio
    """
    upload_path = Path(settings.UPLOAD_DIR)
    upload_path.mkdir(exist_ok=True, parents=True)
    return upload_path.absolute()


def validate_file_extension(filename: str) -> bool:
    """
    Valida si el archivo tiene una extensión permitida.
    
    Args:
        filename (str): Nombre del archivo a validar
        
    Returns:
        bool: True si la extensión es válida, False en caso contrario
    """
    if not filename:
        return False
    
    file_extension = Path(filename).suffix.lower()
    return file_extension in settings.ALLOWED_EXTENSIONS


def get_safe_filename(filename: str) -> str:
    """
    Genera un nombre de archivo seguro eliminando caracteres peligrosos.
    
    Args:
        filename (str): Nombre original del archivo
        
    Returns:
        str: Nombre de archivo seguro
    """
    # Eliminar caracteres peligrosos
    dangerous_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    safe_filename = filename
    
    for char in dangerous_chars:
        safe_filename = safe_filename.replace(char, '_')
    
    return safe_filename 