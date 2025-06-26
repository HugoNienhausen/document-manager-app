# -*- coding: utf-8 -*-
"""
Punto de entrada principal de la aplicación
===========================================

Este archivo es el punto de entrada para ejecutar la aplicación.
Importa y ejecuta la aplicación principal desde el módulo app.
"""

import uvicorn
from app.main import app
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    ) 