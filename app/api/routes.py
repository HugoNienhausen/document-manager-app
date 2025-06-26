# -*- coding: utf-8 -*-
"""
Rutas de la API
===============

Este módulo contiene todas las rutas de la API REST para el manejo
de directorios y archivos PDF.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from typing import List
import time
import os

from ..services import DirectoryService, FileService
from ..models import (
    DirectoryInfo, FileInfo, DirectoryResponse, FileUploadResponse,
    ErrorResponse, HealthCheck
)
from ..config import settings

# Crear router para la API
api_router = APIRouter(prefix="/api/v1", tags=["API"])

# Variables globales para servicios
directory_service = DirectoryService()
file_service = FileService()

# Variable para tracking de uptime
start_time = time.time()


@api_router.get("/health", response_model=HealthCheck)
async def health_check():
    """
    Verificación de salud de la aplicación.
    
    Returns:
        HealthCheck: Estado actual de la aplicación
    """
    uptime = time.time() - start_time
    return HealthCheck(
        status="healthy",
        version="1.0.0",
        uptime=uptime
    )


@api_router.post("/directories", response_model=DirectoryResponse)
async def create_directory(path: str = Form(..., description="Ruta del directorio a crear")):
    """
    Crea un nuevo directorio.
    
    Args:
        path (str): Ruta del directorio a crear (ej: "documentos/trabajo")
        
    Returns:
        DirectoryResponse: Información del directorio creado
        
    Raises:
        HTTPException: Si hay un error al crear el directorio
    """
    try:
        directory_info = await directory_service.create_directory(path)
        return DirectoryResponse(
            message=f"Directorio '{path}' creado exitosamente",
            path=directory_info.path,
            created_at=directory_info.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


@api_router.get("/directories", response_model=List[str])
async def list_directories():
    """
    Lista todos los directorios disponibles.
    
    Returns:
        List[str]: Lista de rutas de directorios
        
    Raises:
        HTTPException: Si hay un error al listar directorios
    """
    try:
        return await directory_service.list_directories()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


@api_router.get("/directories/{path:path}", response_model=DirectoryInfo)
async def get_directory_info(path: str):
    """
    Obtiene información detallada de un directorio.
    
    Args:
        path (str): Ruta del directorio
        
    Returns:
        DirectoryInfo: Información detallada del directorio
        
    Raises:
        HTTPException: Si el directorio no existe o hay un error
    """
    try:
        return await directory_service.get_directory_info(path)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


@api_router.post("/files/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(..., description="Archivo PDF a subir"),
    path: str = Form("", description="Directorio destino")
):
    """
    Sube un archivo PDF a un directorio específico.
    
    Args:
        file (UploadFile): Archivo PDF a subir
        path (str): Ruta del directorio destino (opcional, por defecto raíz)
        
    Returns:
        FileUploadResponse: Información del archivo subido
        
    Raises:
        HTTPException: Si hay un error al subir el archivo
    """
    try:
        # Si path está vacío, usar la raíz
        upload_path = path.strip() if path else ""
        
        file_info = await file_service.upload_file(file, upload_path)
        return FileUploadResponse(
            message=f"PDF '{file_info.name}' subido exitosamente a '{upload_path or 'raíz'}'",
            filename=file_info.name,
            path=file_info.path,
            size=file_info.size,
            uploaded_at=file_info.modified_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


@api_router.get("/files/{path:path}", response_model=List[FileInfo])
async def list_files(path: str):
    """
    Lista todos los archivos PDF en un directorio.
    
    Args:
        path (str): Ruta del directorio
        
    Returns:
        List[FileInfo]: Lista de información de archivos
        
    Raises:
        HTTPException: Si hay un error al listar archivos
    """
    try:
        return await file_service.list_files(path)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


@api_router.get("/files/download/{path:path}")
async def download_file(path: str):
    """
    Descarga un archivo PDF.
    
    Args:
        path (str): Ruta del archivo a descargar
        
    Returns:
        FileResponse: Archivo para descarga
        
    Raises:
        HTTPException: Si el archivo no existe o hay un error
    """
    try:
        print(f"🔍 Intentando descargar archivo: {path}")
        file_path = await file_service.get_file_path(path)
        
        # Verificar que el archivo existe y es accesible
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Archivo '{path}' no encontrado en el servidor"
            )
        
        if not file_path.is_file():
            raise HTTPException(
                status_code=400,
                detail=f"'{path}' no es un archivo válido"
            )
        
        # Verificar que el archivo es legible
        if not os.access(file_path, os.R_OK):
            raise HTTPException(
                status_code=403,
                detail=f"No tienes permisos para leer el archivo '{path}'"
            )
        
        print(f"✅ Archivo encontrado: {file_path}")
        print(f"📏 Tamaño: {file_path.stat().st_size} bytes")
        
        return FileResponse(
            path=str(file_path),
            filename=file_path.name,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=\"{file_path.name}\"",
                "Cache-Control": "no-cache"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al descargar archivo '{path}': {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor al descargar '{path}': {str(e)}"
        )


@api_router.delete("/files/{path:path}")
async def delete_file(path: str):
    """
    Elimina un archivo PDF.
    
    Args:
        path (str): Ruta del archivo a eliminar
        
    Returns:
        dict: Mensaje de confirmación
        
    Raises:
        HTTPException: Si el archivo no existe o hay un error
    """
    try:
        file_path = await file_service.get_file_path(path)
        file_path.unlink()
        return {"message": f"Archivo '{path}' eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


@api_router.delete("/directories/{path:path}")
async def delete_directory(path: str):
    """
    Elimina un directorio y todos sus contenidos.
    
    Args:
        path (str): Ruta del directorio a eliminar
        
    Returns:
        dict: Mensaje de confirmación
        
    Raises:
        HTTPException: Si el directorio no existe o hay un error
    """
    try:
        directory_info = await directory_service.get_directory_info(path)
        safe_path = directory_service._sanitize_path(path)
        full_path = directory_service.upload_path / safe_path
        
        # Eliminar directorio y todo su contenido
        import shutil
        shutil.rmtree(full_path)
        
        return {"message": f"Directorio '{path}' y su contenido eliminados exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        ) 