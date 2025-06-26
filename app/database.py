# -*- coding: utf-8 -*-
"""
Configuración de la base de datos
=================================

Este módulo contiene la configuración de SQLAlchemy para PostgreSQL.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Crear el motor de la base de datos
engine = create_engine(
    settings.database_url,
    echo=settings.DEBUG,  # Mostrar SQL en modo debug
    pool_pre_ping=True,   # Verificar conexión antes de usar
    pool_recycle=300      # Reciclar conexiones cada 5 minutos
)

# Crear la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db():
    """
    Generador de sesiones de base de datos.
    
    Yields:
        Session: Sesión de SQLAlchemy
        
    Raises:
        Exception: Si hay error en la conexión
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Crea todas las tablas en la base de datos.
    
    Raises:
        Exception: Si hay error al crear las tablas
    """
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """
    Elimina todas las tablas de la base de datos.
    
    Raises:
        Exception: Si hay error al eliminar las tablas
    """
    Base.metadata.drop_all(bind=engine) 