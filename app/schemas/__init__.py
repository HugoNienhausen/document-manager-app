# -*- coding: utf-8 -*-
"""
Esquemas Pydantic
=================

Este paquete contiene todos los esquemas Pydantic para la API.
"""

from .document import DocumentCreate, DocumentUpdate, DocumentResponse, DocumentList
from .client import ClientCreate, ClientUpdate, ClientResponse, ClientList
from .category import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryList
from .document_type import DocumentTypeCreate, DocumentTypeUpdate, DocumentTypeResponse, DocumentTypeList

__all__ = [
    "DocumentCreate", "DocumentUpdate", "DocumentResponse", "DocumentList",
    "ClientCreate", "ClientUpdate", "ClientResponse", "ClientList",
    "CategoryCreate", "CategoryUpdate", "CategoryResponse", "CategoryList",
    "DocumentTypeCreate", "DocumentTypeUpdate", "DocumentTypeResponse", "DocumentTypeList"
] 