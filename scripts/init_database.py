#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicialización de la base de datos
============================================

Este script crea las tablas y inserta datos iniciales en la base de datos.
"""

import sys
import os
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

from app.database import engine, create_tables, SessionLocal
from app.models.document_type import DocumentType
from app.models.category import Category
from app.models.client import Client
from app.config import settings


def init_database():
    """Inicializa la base de datos con tablas y datos por defecto."""
    
    print("🚀 Inicializando base de datos...")
    print(f"📊 URL de conexión: {settings.database_url}")
    
    try:
        # Crear tablas
        print("📋 Creando tablas...")
        create_tables()
        print("✅ Tablas creadas exitosamente")
        
        # Crear sesión de base de datos
        db = SessionLocal()
        
        try:
            # Insertar tipos de documentos por defecto
            print("📄 Insertando tipos de documentos...")
            document_types = [
                DocumentType(name="Factura", description="Documentos de facturación", icon="fas fa-file-invoice"),
                DocumentType(name="Contrato", description="Contratos y acuerdos", icon="fas fa-file-contract"),
                DocumentType(name="Recibo", description="Recibos de pago", icon="fas fa-receipt"),
                DocumentType(name="Identificación", description="Documentos de identificación", icon="fas fa-id-card"),
                DocumentType(name="Certificado", description="Certificados oficiales", icon="fas fa-certificate"),
                DocumentType(name="Otro", description="Otros tipos de documentos", icon="fas fa-file-pdf")
            ]
            
            for doc_type in document_types:
                existing = db.query(DocumentType).filter(DocumentType.name == doc_type.name).first()
                if not existing:
                    db.add(doc_type)
                    print(f"  ➕ Tipo de documento: {doc_type.name}")
            
            # Insertar categorías por defecto
            print("📁 Insertando categorías...")
            categories = [
                Category(name="Financiero", description="Documentos relacionados con finanzas", color="#10b981"),
                Category(name="Legal", description="Documentos legales y contratos", color="#3b82f6"),
                Category(name="Personal", description="Documentos personales", color="#f59e0b"),
                Category(name="Laboral", description="Documentos relacionados con trabajo", color="#8b5cf6"),
                Category(name="Médico", description="Documentos médicos", color="#ef4444"),
                Category(name="Otros", description="Otras categorías", color="#6b7280")
            ]
            
            for category in categories:
                existing = db.query(Category).filter(Category.name == category.name).first()
                if not existing:
                    db.add(category)
                    print(f"  ➕ Categoría: {category.name}")
            
            # Insertar cliente de ejemplo
            print("👤 Insertando cliente de ejemplo...")
            example_client = Client(
                name="Cliente Ejemplo",
                email="ejemplo@cliente.com",
                phone="+34 123 456 789",
                address="Calle Ejemplo, 123, Madrid",
                notes="Cliente de ejemplo para pruebas"
            )
            
            existing_client = db.query(Client).filter(Client.email == example_client.email).first()
            if not existing_client:
                db.add(example_client)
                print("  ➕ Cliente: Cliente Ejemplo")
            
            # Confirmar cambios
            db.commit()
            print("✅ Datos iniciales insertados exitosamente")
            
            # Mostrar estadísticas
            print("\n📊 Estadísticas de la base de datos:")
            doc_types_count = db.query(DocumentType).count()
            categories_count = db.query(Category).count()
            clients_count = db.query(Client).count()
            
            print(f"  📄 Tipos de documentos: {doc_types_count}")
            print(f"  📁 Categorías: {categories_count}")
            print(f"  👤 Clientes: {clients_count}")
            
        except Exception as e:
            db.rollback()
            print(f"❌ Error al insertar datos: {str(e)}")
            raise
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {str(e)}")
        sys.exit(1)
    
    print("\n🎉 Base de datos inicializada correctamente!")
    print("🌐 Puedes iniciar la aplicación con: python main.py")


if __name__ == "__main__":
    init_database() 