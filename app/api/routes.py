# -*- coding: utf-8 -*-
"""
Rutas de la API
===============

Este módulo contiene todas las rutas de la API REST para el manejo
de directorios y archivos PDF.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from typing import List, Optional
import time
import os

from ..services import DirectoryService, FileService, DocumentService
from ..pydantic_models import (
    DirectoryInfo, FileInfo, DirectoryResponse, FileUploadResponse,
    ErrorResponse, HealthCheck, DocumentUploadResponse, DocumentResponse,
    DocumentTypeResponse, ClientResponse, CategoryResponse,
    DocumentTypeCreate, DocumentTypeUpdate, CategoryCreate, CategoryUpdate,
    ClientCreate, ClientUpdate
)
from ..config import settings

# Crear router para la API
api_router = APIRouter(prefix="/api/v1", tags=["API"])

# Variables globales para servicios
directory_service = DirectoryService()
file_service = FileService()
document_service = DocumentService()

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
                detail=f"No tienes permisos para acceder al archivo '{path}'"
            )
        
        # Obtener información del archivo
        stat = file_path.stat()
        file_size = stat.st_size
        print(f"✅ Archivo encontrado: {file_path}")
        print(f"📏 Tamaño: {file_size} bytes")
        
        # Retornar el archivo para descarga
        return FileResponse(
            path=str(file_path),
            filename=file_path.name,
            media_type="application/pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al descargar archivo '{path}': {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


@api_router.get("/files/{path:path}", response_model=List[FileInfo])
async def list_files(path: str):
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
        return await file_service.list_files(path)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


@api_router.delete("/files/{path:path}")
async def delete_file(path: str):
    """
    Elimina un archivo PDF. Si el archivo está registrado en la base de datos,
    también elimina el registro correspondiente.
    
    Args:
        path (str): Ruta del archivo a eliminar
        
    Returns:
        dict: Mensaje de confirmación
        
    Raises:
        HTTPException: Si el archivo no existe o hay un error
    """
    try:
        # Intentar eliminar como documento (con metadatos)
        try:
            return await document_service.delete_document(path)
        except HTTPException as e:
            if e.status_code == 404:
                # Si no está en la base de datos, eliminar solo del sistema de archivos
                file_path = await file_service.get_file_path(path)
                
                # Verificar que el archivo existe
                if not file_path.exists():
                    raise HTTPException(
                        status_code=404,
                        detail=f"Archivo '{path}' no encontrado"
                    )
                
                # Eliminar el archivo
                file_path.unlink()
                
                return {
                    "message": f"Archivo '{path}' eliminado exitosamente del sistema de archivos",
                    "deleted_at": time.time(),
                    "from_database": False
                }
            else:
                raise e
        
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
    Elimina un directorio y todo su contenido.
    
    Args:
        path (str): Ruta del directorio a eliminar
        
    Returns:
        dict: Mensaje de confirmación
        
    Raises:
        HTTPException: Si el directorio no existe o hay un error
    """
    try:
        from pathlib import Path
        from ..config import get_upload_path
        
        upload_path = get_upload_path()
        full_path = upload_path / path
        
        # Verificar que el directorio existe
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
        
        # Eliminar el directorio y todo su contenido
        import shutil
        shutil.rmtree(full_path)
        
        return {
            "message": f"Directorio '{path}' y todo su contenido eliminado exitosamente",
            "deleted_at": time.time()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


# ============================================================================
# RUTAS PARA DOCUMENTOS CON METADATOS
# ============================================================================

@api_router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document_with_metadata(
    file: UploadFile = File(..., description="Archivo PDF a subir"),
    path: str = Form(..., description="Directorio destino"),
    document_type_id: int = Form(..., description="ID del tipo de documento"),
    category_id: int = Form(..., description="ID de la categoría"),
    client_id: Optional[int] = Form(None, description="ID del cliente (opcional)"),
    upload_date: Optional[str] = Form(None, description="Fecha de subida (YYYY-MM-DD HH:MM:SS)")
):
    """
    Sube un documento PDF y lo registra en la base de datos con metadatos.
    
    Args:
        file (UploadFile): Archivo PDF a subir
        path (str): Ruta del directorio destino
        document_type_id (int): ID del tipo de documento
        category_id (int): ID de la categoría
        client_id (int, optional): ID del cliente
        upload_date (str, optional): Fecha de subida en formato YYYY-MM-DD HH:MM:SS
        
    Returns:
        DocumentUploadResponse: Información del documento creado
        
    Raises:
        HTTPException: Si hay un error al subir el documento
    """
    try:
        from datetime import datetime
        
        # Parsear la fecha si se proporciona
        parsed_upload_date = None
        if upload_date:
            try:
                parsed_upload_date = datetime.fromisoformat(upload_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Formato de fecha inválido. Use YYYY-MM-DD HH:MM:SS"
                )
        
        # Convertir client_id a None si es 0 o negativo
        if client_id is not None and client_id <= 0:
            client_id = None
        
        document = await document_service.upload_document_with_metadata(
            file=file,
            path=path,
            document_type_id=document_type_id,
            category_id=category_id,
            client_id=client_id,
            upload_date=parsed_upload_date
        )
        
        return DocumentUploadResponse(
            message=f"Documento '{document.filename}' subido y registrado exitosamente",
            document=document,
            uploaded_at=document.upload_date
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


@api_router.get("/documents/types", response_model=List[DocumentTypeResponse])
async def get_document_types():
    """
    Obtiene todos los tipos de documento disponibles.
    
    Returns:
        List[DocumentTypeResponse]: Lista de tipos de documento
        
    Raises:
        HTTPException: Si hay un error al obtener los tipos
    """
    try:
        return await document_service.get_document_types()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


@api_router.get("/documents/clients", response_model=List[ClientResponse])
async def get_clients():
    """
    Obtiene todos los clientes disponibles.
    
    Returns:
        List[ClientResponse]: Lista de clientes
        
    Raises:
        HTTPException: Si hay un error al obtener los clientes
    """
    try:
        return await document_service.get_clients()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


@api_router.get("/documents/categories", response_model=List[CategoryResponse])
async def get_categories():
    """
    Obtiene todas las categorías disponibles.
    
    Returns:
        List[CategoryResponse]: Lista de categorías
        
    Raises:
        HTTPException: Si hay un error al obtener las categorías
    """
    try:
        return await document_service.get_categories()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


@api_router.delete("/documents/{path:path}")
async def delete_document(path: str):
    """
    Elimina un documento tanto del sistema de archivos como de la base de datos.
    
    Args:
        path (str): Ruta del archivo a eliminar (ej: "Documentos/archivo.pdf")
        
    Returns:
        dict: Información del documento eliminado
        
    Raises:
        HTTPException: Si el documento no existe o hay un error
    """
    try:
        return await document_service.delete_document(path)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


# ============================================================================
# RUTAS CRUD PARA METADATOS
# ============================================================================

# Document Types CRUD
@api_router.post("/metadata/document-types", response_model=DocumentTypeResponse)
async def create_document_type(document_type: DocumentTypeCreate):
    """
    Crea un nuevo tipo de documento.
    
    Args:
        document_type (DocumentTypeCreate): Datos del tipo de documento
        
    Returns:
        DocumentTypeResponse: Tipo de documento creado
    """
    try:
        return await document_service.create_document_type(document_type)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@api_router.put("/metadata/document-types/{type_id}", response_model=DocumentTypeResponse)
async def update_document_type(type_id: int, document_type: DocumentTypeUpdate):
    """
    Actualiza un tipo de documento existente.
    
    Args:
        type_id (int): ID del tipo de documento
        document_type (DocumentTypeUpdate): Datos actualizados
        
    Returns:
        DocumentTypeResponse: Tipo de documento actualizado
    """
    try:
        return await document_service.update_document_type(type_id, document_type)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@api_router.delete("/metadata/document-types/{type_id}")
async def delete_document_type(type_id: int):
    """
    Elimina un tipo de documento.
    
    Args:
        type_id (int): ID del tipo de documento
        
    Returns:
        dict: Mensaje de confirmación
    """
    try:
        await document_service.delete_document_type(type_id)
        return {
            "message": f"Tipo de documento con ID {type_id} eliminado exitosamente",
            "deleted_at": time.time()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

# Categories CRUD
@api_router.post("/metadata/categories", response_model=CategoryResponse)
async def create_category(category: CategoryCreate):
    """
    Crea una nueva categoría.
    
    Args:
        category (CategoryCreate): Datos de la categoría
        
    Returns:
        CategoryResponse: Categoría creada
    """
    try:
        return await document_service.create_category(category)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@api_router.put("/metadata/categories/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, category: CategoryUpdate):
    """
    Actualiza una categoría existente.
    
    Args:
        category_id (int): ID de la categoría
        category (CategoryUpdate): Datos actualizados
        
    Returns:
        CategoryResponse: Categoría actualizada
    """
    try:
        return await document_service.update_category(category_id, category)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@api_router.delete("/metadata/categories/{category_id}")
async def delete_category(category_id: int):
    """
    Elimina una categoría.
    
    Args:
        category_id (int): ID de la categoría
        
    Returns:
        dict: Mensaje de confirmación
    """
    try:
        await document_service.delete_category(category_id)
        return {
            "message": f"Categoría con ID {category_id} eliminada exitosamente",
            "deleted_at": time.time()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

# Clients CRUD
@api_router.post("/metadata/clients", response_model=ClientResponse)
async def create_client(client: ClientCreate):
    """
    Crea un nuevo cliente.
    
    Args:
        client (ClientCreate): Datos del cliente
        
    Returns:
        ClientResponse: Cliente creado
    """
    try:
        return await document_service.create_client(client)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@api_router.put("/metadata/clients/{client_id}", response_model=ClientResponse)
async def update_client(client_id: int, client: ClientUpdate):
    """
    Actualiza un cliente existente.
    
    Args:
        client_id (int): ID del cliente
        client (ClientUpdate): Datos actualizados
        
    Returns:
        ClientResponse: Cliente actualizado
    """
    try:
        return await document_service.update_client(client_id, client)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@api_router.delete("/metadata/clients/{client_id}")
async def delete_client(client_id: int):
    """
    Elimina un cliente.
    
    Args:
        client_id (int): ID del cliente
        
    Returns:
        dict: Mensaje de confirmación
    """
    try:
        await document_service.delete_client(client_id)
        return {
            "message": f"Cliente con ID {client_id} eliminado exitosamente",
            "deleted_at": time.time()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        ) 