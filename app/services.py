# -*- coding: utf-8 -*-
"""
Servicios de la aplicación
==========================

Este módulo contiene la lógica de negocio para el manejo de directorios
y archivos, separada de las rutas de la API.
"""

import os
import shutil
import aiofiles
from pathlib import Path
from typing import List, Optional, Tuple
from datetime import datetime
from fastapi import UploadFile, HTTPException

from .config import settings, get_upload_path, validate_file_extension, get_safe_filename
from .models import DirectoryInfo, FileInfo


class DirectoryService:
    """
    Servicio para manejo de directorios.
    
    Contiene toda la lógica de negocio relacionada con la creación,
    listado y gestión de directorios.
    """
    
    def __init__(self):
        """Inicializa el servicio con la ruta base de uploads."""
        self.upload_path = get_upload_path()
    
    async def create_directory(self, path: str) -> DirectoryInfo:
        """
        Crea un nuevo directorio.
        
        Args:
            path (str): Ruta del directorio a crear
            
        Returns:
            DirectoryInfo: Información del directorio creado
            
        Raises:
            HTTPException: Si hay un error al crear el directorio
        """
        try:
            # Validar y limpiar la ruta
            safe_path = self._sanitize_path(path)
            full_path = self.upload_path / safe_path
            
            # Crear el directorio
            full_path.mkdir(parents=True, exist_ok=True)
            
            # Obtener información del directorio
            stat = full_path.stat()
            
            return DirectoryInfo(
                name=full_path.name,
                path=str(safe_path),
                files_count=len([f for f in full_path.iterdir() if f.is_file()]),
                created_at=datetime.fromtimestamp(stat.st_ctime)
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error al crear directorio '{path}': {str(e)}"
            )
    
    async def list_directories(self) -> List[str]:
        """
        Lista todos los directorios disponibles.
        
        Returns:
            List[str]: Lista de rutas de directorios
            
        Raises:
            HTTPException: Si hay un error al listar directorios
        """
        try:
            directories = []
            
            for root, dirs, files in os.walk(self.upload_path):
                for dir_name in dirs:
                    rel_path = os.path.relpath(
                        os.path.join(root, dir_name), 
                        self.upload_path
                    )
                    directories.append(rel_path)
            
            return directories
            
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error al listar directorios: {str(e)}"
            )
    
    async def get_directory_info(self, path: str) -> DirectoryInfo:
        """
        Obtiene información detallada de un directorio.
        
        Args:
            path (str): Ruta del directorio
            
        Returns:
            DirectoryInfo: Información del directorio
            
        Raises:
            HTTPException: Si el directorio no existe o hay un error
        """
        try:
            safe_path = self._sanitize_path(path)
            full_path = self.upload_path / safe_path
            
            if not full_path.exists():
                raise HTTPException(
                    status_code=404,
                    detail=f"Directorio '{path}' no encontrado"
                )
            
            if not full_path.is_dir():
                raise HTTPException(
                    status_code=400,
                    detail=f"'{path}' no es un directorio"
                )
            
            stat = full_path.stat()
            files_count = len([f for f in full_path.iterdir() if f.is_file()])
            
            return DirectoryInfo(
                name=full_path.name,
                path=str(safe_path),
                files_count=files_count,
                created_at=datetime.fromtimestamp(stat.st_ctime)
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error al obtener información del directorio: {str(e)}"
            )
    
    def _sanitize_path(self, path: str) -> Path:
        """
        Sanitiza una ruta para evitar ataques de path traversal.
        
        Args:
            path (str): Ruta a sanitizar
            
        Returns:
            Path: Ruta sanitizada
            
        Raises:
            HTTPException: Si la ruta es inválida
        """
        # Limpiar la ruta de caracteres peligrosos
        clean_path = Path(path)
        
        # Verificar que no contenga componentes peligrosos
        for part in clean_path.parts:
            if part in ['.', '..'] or part.startswith('/'):
                raise HTTPException(
                    status_code=400,
                    detail="Ruta inválida: no puede contener '..' o rutas absolutas"
                )
        
        # Construir la ruta completa
        full_path = self.upload_path / clean_path
        
        # Verificar que la ruta normalizada no escape del directorio base
        try:
            full_path.resolve().relative_to(self.upload_path.resolve())
        except (ValueError, RuntimeError):
            raise HTTPException(
                status_code=400,
                detail="Ruta inválida: no puede salir del directorio base"
            )
        
        return clean_path


class FileService:
    """
    Servicio para manejo de archivos.
    
    Contiene toda la lógica de negocio relacionada con la subida,
    listado y descarga de archivos.
    """
    
    def __init__(self):
        """Inicializa el servicio con la ruta base de uploads."""
        self.upload_path = get_upload_path()
    
    async def upload_file(self, file: UploadFile, path: str) -> FileInfo:
        """
        Sube un archivo a un directorio específico.
        
        Args:
            file (UploadFile): Archivo a subir
            path (str): Ruta del directorio destino
            
        Returns:
            FileInfo: Información del archivo subido
            
        Raises:
            HTTPException: Si hay un error al subir el archivo
        """
        try:
            # Validar el archivo
            if not file.filename:
                raise HTTPException(
                    status_code=400,
                    detail="Nombre de archivo no válido"
                )
            
            if not validate_file_extension(file.filename):
                raise HTTPException(
                    status_code=400,
                    detail=f"Solo se permiten archivos con extensiones: {settings.ALLOWED_EXTENSIONS}"
                )
            
            # Crear el directorio si no existe
            safe_path = self._sanitize_path(path)
            full_dir_path = self.upload_path / safe_path
            full_dir_path.mkdir(parents=True, exist_ok=True)
            
            # Generar nombre seguro para el archivo
            safe_filename = get_safe_filename(file.filename)
            file_path = full_dir_path / safe_filename
            
            # Verificar si el archivo ya existe
            if file_path.exists():
                raise HTTPException(
                    status_code=409,
                    detail=f"El archivo '{safe_filename}' ya existe en el directorio"
                )
            
            # Guardar el archivo
            content = await file.read()
            
            # Verificar tamaño del archivo
            if len(content) > settings.MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=413,
                    detail=f"El archivo excede el tamaño máximo de {settings.MAX_FILE_SIZE} bytes"
                )
            
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(content)
            
            # Obtener información del archivo
            stat = file_path.stat()
            
            return FileInfo(
                name=safe_filename,
                path=str(safe_path / safe_filename),
                size=len(content),
                extension=file_path.suffix,
                modified_at=datetime.fromtimestamp(stat.st_mtime)
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error al subir archivo: {str(e)}"
            )
    
    async def list_files(self, path: str) -> List[FileInfo]:
        """
        Lista todos los archivos en un directorio.
        
        Args:
            path (str): Ruta del directorio
            
        Returns:
            List[FileInfo]: Lista de información de archivos
            
        Raises:
            HTTPException: Si hay un error al listar archivos
        """
        try:
            safe_path = self._sanitize_path(path)
            full_path = self.upload_path / safe_path
            
            if not full_path.exists():
                raise HTTPException(
                    status_code=404,
                    detail=f"Directorio '{path}' no encontrado"
                )
            
            if not full_path.is_dir():
                raise HTTPException(
                    status_code=400,
                    detail=f"'{path}' no es un directorio"
                )
            
            files = []
            for file_path in full_path.iterdir():
                if file_path.is_file() and validate_file_extension(file_path.name):
                    stat = file_path.stat()
                    files.append(FileInfo(
                        name=file_path.name,
                        path=str(safe_path / file_path.name),
                        size=stat.st_size,
                        extension=file_path.suffix,
                        modified_at=datetime.fromtimestamp(stat.st_mtime)
                    ))
            
            return files
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error al listar archivos: {str(e)}"
            )
    
    async def get_file_path(self, path: str) -> Path:
        """
        Obtiene la ruta completa de un archivo.
        
        Args:
            path (str): Ruta del archivo
            
        Returns:
            Path: Ruta completa del archivo
            
        Raises:
            HTTPException: Si el archivo no existe
        """
        try:
            safe_path = self._sanitize_path(path)
            full_path = self.upload_path / safe_path
            
            if not full_path.exists():
                raise HTTPException(
                    status_code=404,
                    detail=f"Archivo '{path}' no encontrado"
                )
            
            if not full_path.is_file():
                raise HTTPException(
                    status_code=400,
                    detail=f"'{path}' no es un archivo"
                )
            
            return full_path
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error al obtener archivo: {str(e)}"
            )
    
    def _sanitize_path(self, path: str) -> Path:
        """
        Sanitiza una ruta para evitar ataques de path traversal.
        
        Args:
            path (str): Ruta a sanitizar
            
        Returns:
            Path: Ruta sanitizada
            
        Raises:
            HTTPException: Si la ruta es inválida
        """
        # Limpiar la ruta de caracteres peligrosos
        clean_path = Path(path)
        
        # Verificar que no contenga componentes peligrosos
        for part in clean_path.parts:
            if part in ['.', '..'] or part.startswith('/'):
                raise HTTPException(
                    status_code=400,
                    detail="Ruta inválida: no puede contener '..' o rutas absolutas"
                )
        
        # Construir la ruta completa
        full_path = self.upload_path / clean_path
        
        # Verificar que la ruta normalizada no escape del directorio base
        try:
            full_path.resolve().relative_to(self.upload_path.resolve())
        except (ValueError, RuntimeError):
            raise HTTPException(
                status_code=400,
                detail="Ruta inválida: no puede salir del directorio base"
            )
        
        return clean_path 