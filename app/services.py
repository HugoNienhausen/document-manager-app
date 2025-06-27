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
from .pydantic_models import DirectoryInfo, FileInfo


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
            path (str): Ruta del archivo (ej: "Documentos/archivo.pdf")
            
        Returns:
            Path: Ruta completa del archivo
            
        Raises:
            HTTPException: Si el archivo no existe
        """
        try:
            print(f"🔍 Buscando archivo: {path}")
            
            # Separar el directorio del nombre del archivo
            path_parts = Path(path).parts
            if len(path_parts) < 2:
                raise HTTPException(
                    status_code=400,
                    detail="Ruta de archivo inválida: debe incluir directorio y nombre de archivo"
                )
            
            # El último elemento es el nombre del archivo
            filename = path_parts[-1]
            # El resto es el directorio
            directory_parts = path_parts[:-1]
            directory_path = Path(*directory_parts)
            
            print(f"📁 Directorio: {directory_path}")
            print(f"📄 Archivo: {filename}")
            
            # Sanitizar el directorio
            safe_directory = self._sanitize_path(str(directory_path))
            full_path = self.upload_path / safe_directory / filename
            
            print(f"📂 Ruta completa: {full_path}")
            print(f"📂 Ruta absoluta: {full_path.absolute()}")
            print(f"📂 Existe: {full_path.exists()}")
            
            if not full_path.exists():
                print(f"❌ Archivo no encontrado: {full_path}")
                raise HTTPException(
                    status_code=404,
                    detail=f"Archivo '{path}' no encontrado"
                )
            
            if not full_path.is_file():
                print(f"❌ No es un archivo: {full_path}")
                raise HTTPException(
                    status_code=400,
                    detail=f"'{path}' no es un archivo"
                )
            
            print(f"✅ Archivo encontrado: {full_path}")
            return full_path
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"❌ Error al obtener archivo '{path}': {str(e)}")
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


class DocumentService:
    """
    Servicio para manejo de documentos con base de datos.
    
    Contiene toda la lógica de negocio relacionada con la subida,
    registro y gestión de documentos con metadatos en la base de datos.
    """
    
    def __init__(self):
        """Inicializa el servicio con la ruta base de uploads."""
        self.upload_path = get_upload_path()
    
    async def upload_document_with_metadata(
        self, 
        file: UploadFile, 
        path: str, 
        document_type_id: int,
        category_id: int,
        client_id: Optional[int] = None,
        upload_date: Optional[datetime] = None
    ):
        """
        Sube un documento y lo registra en la base de datos con metadatos.
        
        Args:
            file (UploadFile): Archivo a subir
            path (str): Ruta del directorio destino
            document_type_id (int): ID del tipo de documento
            category_id (int): ID de la categoría
            client_id (Optional[int]): ID del cliente (opcional)
            upload_date (Optional[datetime]): Fecha de subida (automática si no se especifica)
            
        Returns:
            DocumentResponse: Información del documento creado
            
        Raises:
            HTTPException: Si hay un error al subir el documento
        """
        from .database import get_db
        from .models.document import Document
        from .models.document_type import DocumentType
        from .models.category import Category
        from .models.client import Client
        from .pydantic_models import DocumentResponse
        
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
            
            # Leer el contenido del archivo
            content = await file.read()
            
            # Verificar tamaño del archivo
            if len(content) > settings.MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=413,
                    detail=f"El archivo excede el tamaño máximo de {settings.MAX_FILE_SIZE} bytes"
                )
            
            # Generar hash del archivo
            file_hash = Document.generate_file_hash_from_content(content)
            
            # Verificar si ya existe un documento con el mismo hash
            db = next(get_db())
            existing_document = db.query(Document).filter(Document.file_hash == file_hash).first()
            if existing_document:
                raise HTTPException(
                    status_code=409,
                    detail=f"Ya existe un documento con el mismo contenido (hash: {file_hash[:8]}...)"
                )
            
            # Verificar que existan los tipos, categorías y cliente
            document_type = db.query(DocumentType).filter(DocumentType.id == document_type_id).first()
            if not document_type:
                raise HTTPException(
                    status_code=400,
                    detail=f"Tipo de documento con ID {document_type_id} no encontrado"
                )
            
            category = db.query(Category).filter(Category.id == category_id).first()
            if not category:
                raise HTTPException(
                    status_code=400,
                    detail=f"Categoría con ID {category_id} no encontrada"
                )
            
            client = None
            if client_id:
                client = db.query(Client).filter(Client.id == client_id).first()
                if not client:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Cliente con ID {client_id} no encontrado"
                    )
            
            # Guardar el archivo
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(content)
            
            # Crear el registro en la base de datos
            document = Document(
                filename=safe_filename,
                file_hash=file_hash,
                document_type_id=document_type_id,
                client_id=client_id,
                category_id=category_id,
                local_path=str(file_path),
                file_size=len(content),
                upload_date=upload_date or datetime.now()
            )
            
            db.add(document)
            db.commit()
            db.refresh(document)
            
            # Obtener información relacionada para la respuesta
            document_type_name = document_type.name
            category_name = category.name
            client_name = client.name if client else None
            
            return DocumentResponse(
                id=document.id,
                filename=document.filename,
                file_hash=document.file_hash,
                document_type=document_type_name,
                client=client_name,
                category=category_name,
                local_path=document.local_path,
                file_size=document.file_size,
                upload_date=document.upload_date,
                created_at=document.created_at
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error al subir documento: {str(e)}"
            )
    
    async def get_document_types(self):
        """
        Obtiene todos los tipos de documento disponibles.
        
        Returns:
            List[DocumentTypeResponse]: Lista de tipos de documento
        """
        from .database import get_db
        from .models.document_type import DocumentType
        from .pydantic_models import DocumentTypeResponse
        
        try:
            db = next(get_db())
            document_types = db.query(DocumentType).all()
            
            return [
                DocumentTypeResponse(
                    id=dt.id,
                    name=dt.name,
                    description=dt.description
                )
                for dt in document_types
            ]
            
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error al obtener tipos de documento: {str(e)}"
            )
    
    async def get_clients(self):
        """
        Obtiene todos los clientes disponibles.
        
        Returns:
            List[ClientResponse]: Lista de clientes
        """
        from .database import get_db
        from .models.client import Client
        from .pydantic_models import ClientResponse
        
        try:
            db = next(get_db())
            clients = db.query(Client).all()
            
            return [
                ClientResponse(
                    id=c.id,
                    name=c.name,
                    email=c.email,
                    phone=c.phone
                )
                for c in clients
            ]
            
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error al obtener clientes: {str(e)}"
            )
    
    async def get_categories(self):
        """
        Obtiene todas las categorías disponibles.
        
        Returns:
            List[CategoryResponse]: Lista de categorías
        """
        from .database import get_db
        from .models.category import Category
        from .pydantic_models import CategoryResponse
        
        try:
            db = next(get_db())
            categories = db.query(Category).all()
            
            return [
                CategoryResponse(
                    id=c.id,
                    name=c.name,
                    description=c.description
                )
                for c in categories
            ]
            
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error al obtener categorías: {str(e)}"
            )
    
    async def delete_document(self, path: str):
        """
        Elimina un documento de la base de datos y del sistema de archivos.
        
        Args:
            path (str): Ruta del archivo a eliminar (ej: "Documentos/archivo.pdf")
            
        Returns:
            dict: Información del documento eliminado
            
        Raises:
            HTTPException: Si el documento no existe o hay un error
        """
        from .database import get_db
        from .models.document import Document
        
        try:
            # Obtener la ruta completa del archivo
            file_path = await self._get_file_path(path)
            
            # Buscar el documento en la base de datos por la ruta local
            db = next(get_db())
            document = db.query(Document).filter(Document.local_path == str(file_path)).first()
            
            if not document:
                # Si no existe en la base de datos, solo eliminar el archivo
                if file_path.exists():
                    file_path.unlink()
                    return {
                        "message": f"Archivo '{path}' eliminado del sistema de archivos (no estaba registrado en la base de datos)",
                        "deleted_at": datetime.now()
                    }
                else:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Archivo '{path}' no encontrado"
                    )
            
            # Eliminar el archivo del sistema de archivos
            if file_path.exists():
                file_path.unlink()
            
            # Guardar información del documento antes de eliminarlo
            deleted_document = {
                "id": document.id,
                "filename": document.filename,
                "file_hash": document.file_hash,
                "local_path": document.local_path,
                "file_size": document.file_size,
                "upload_date": document.upload_date
            }
            
            # Eliminar el registro de la base de datos
            db.delete(document)
            db.commit()
            
            return {
                "message": f"Documento '{path}' eliminado exitosamente",
                "deleted_document": deleted_document,
                "deleted_at": datetime.now()
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error al eliminar documento: {str(e)}"
            )
    
    async def _get_file_path(self, path: str) -> Path:
        """
        Obtiene la ruta completa de un archivo.
        
        Args:
            path (str): Ruta del archivo (ej: "Documentos/archivo.pdf")
            
        Returns:
            Path: Ruta completa del archivo
            
        Raises:
            HTTPException: Si el archivo no existe
        """
        try:
            print(f"🔍 Buscando archivo: {path}")
            
            # Separar el directorio del nombre del archivo
            path_parts = Path(path).parts
            if len(path_parts) < 2:
                raise HTTPException(
                    status_code=400,
                    detail="Ruta de archivo inválida: debe incluir directorio y nombre de archivo"
                )
            
            # El último elemento es el nombre del archivo
            filename = path_parts[-1]
            # El resto es el directorio
            directory_parts = path_parts[:-1]
            directory_path = Path(*directory_parts)
            
            print(f"📁 Directorio: {directory_path}")
            print(f"📄 Archivo: {filename}")
            
            # Sanitizar el directorio
            safe_directory = self._sanitize_path(str(directory_path))
            full_path = self.upload_path / safe_directory / filename
            
            print(f"📂 Ruta completa: {full_path}")
            print(f"📂 Ruta absoluta: {full_path.absolute()}")
            print(f"📂 Existe: {full_path.exists()}")
            
            if not full_path.exists():
                print(f"❌ Archivo no encontrado: {full_path}")
                raise HTTPException(
                    status_code=404,
                    detail=f"Archivo '{path}' no encontrado"
                )
            
            if not full_path.is_file():
                print(f"❌ No es un archivo: {full_path}")
                raise HTTPException(
                    status_code=400,
                    detail=f"'{path}' no es un archivo"
                )
            
            print(f"✅ Archivo encontrado: {full_path}")
            return full_path
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"❌ Error al obtener archivo '{path}': {str(e)}")
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