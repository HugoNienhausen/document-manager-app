# -*- coding: utf-8 -*-
"""
Modelos SQLAlchemy de la aplicación
==================================

Este paquete contiene todos los modelos SQLAlchemy de la aplicación.
Los modelos Pydantic están en el archivo models.py principal.
"""

# Importar modelos SQLAlchemy
from .document import Document
from .client import Client
from .category import Category
from .document_type import DocumentType

__all__ = [
    # Modelos SQLAlchemy
    "Document", "Client", "Category", "DocumentType"
] 