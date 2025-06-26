# -*- coding: utf-8 -*-
"""
Aplicación principal FastAPI
============================

Este módulo contiene la configuración principal de la aplicación FastAPI
y la integración de todos los componentes.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import time
from pathlib import Path

from .config import settings, get_upload_path
from .api.routes import api_router
from .models import HealthCheck

# Crear la aplicación FastAPI
app = FastAPI(
    title="Gestor de PDFs",
    description="Aplicación para gestionar directorios y archivos PDF de forma organizada",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir rutas de la API
app.include_router(api_router)

# Variable para tracking de uptime
start_time = time.time()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Página principal de la aplicación.
    
    Returns:
        HTMLResponse: Página HTML del frontend
    """
    try:
        # Leer el archivo HTML del frontend
        html_file = Path("static/index.html")
        if html_file.exists():
            with open(html_file, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        else:
            # Fallback si no existe el archivo HTML
            return HTMLResponse(content="""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Gestor de PDFs - API</title>
                <meta charset="utf-8">
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                    .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    h1 { color: #333; text-align: center; }
                    .api-links { margin: 30px 0; }
                    .api-links a { display: block; padding: 15px; margin: 10px 0; background: #007bff; color: white; text-decoration: none; border-radius: 5px; text-align: center; }
                    .api-links a:hover { background: #0056b3; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>📁 Gestor de PDFs - API</h1>
                    <p style="text-align: center; color: #666;">La aplicación está funcionando correctamente. Usa los siguientes enlaces para acceder a la documentación de la API:</p>
                    <div class="api-links">
                        <a href="/docs">📖 Documentación Swagger UI</a>
                        <a href="/redoc">📚 Documentación ReDoc</a>
                        <a href="/api/v1/health">🏥 Estado de la aplicación</a>
                    </div>
                </div>
            </body>
            </html>
            """)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar la página principal: {str(e)}")


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """
    Verificación de salud de la aplicación (endpoint legacy).
    
    Returns:
        HealthCheck: Estado actual de la aplicación
    """
    uptime = time.time() - start_time
    return HealthCheck(
        status="healthy",
        version="1.0.0",
        uptime=uptime
    )


@app.on_event("startup")
async def startup_event():
    """
    Evento que se ejecuta al iniciar la aplicación.
    
    Crea los directorios necesarios y realiza configuraciones iniciales.
    """
    try:
        # Crear directorio de uploads
        upload_path = get_upload_path()
        print(f"✅ Directorio de uploads creado: {upload_path}")
        
        # Crear directorio static si no existe
        static_path = Path("static")
        static_path.mkdir(exist_ok=True)
        print(f"✅ Directorio static verificado: {static_path}")
        
        print("🚀 Aplicación iniciada correctamente")
        print(f"📖 Documentación disponible en: http://{settings.HOST}:{settings.PORT}/docs")
        print(f"🌐 Frontend disponible en: http://{settings.HOST}:{settings.PORT}/")
        
    except Exception as e:
        print(f"❌ Error durante el inicio: {str(e)}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento que se ejecuta al cerrar la aplicación.
    """
    print("🛑 Aplicación cerrada")


# Manejo de errores personalizado
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """
    Manejador personalizado para errores 404.
    """
    return HTMLResponse(
        content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>404 - Página no encontrada</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; text-align: center; }
                .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #e74c3c; font-size: 3rem; margin-bottom: 20px; }
                p { color: #666; font-size: 1.2rem; }
                a { color: #3498db; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>404</h1>
                <p>La página que buscas no existe.</p>
                <p><a href="/">← Volver al inicio</a></p>
            </div>
        </body>
        </html>
        """,
        status_code=404
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    ) 