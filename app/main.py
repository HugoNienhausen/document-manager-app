# -*- coding: utf-8 -*-
"""
FastAPI Main Application
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
from .pydantic_models import HealthCheck

# Create FastAPI application
app = FastAPI(
    title="PDF Manager",
    description="Application for managing directories and PDF files",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routes
app.include_router(api_router)

# Uptime tracking
start_time = time.time()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Main page of the application."""
    try:
        html_file = Path("static/index.html")
        if html_file.exists():
            with open(html_file, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        else:
            # Fallback if HTML file doesn't exist
            return HTMLResponse(content="""
            <!DOCTYPE html>
            <html>
            <head>
                <title>PDF Manager - API</title>
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
                    <h1>PDF Manager - API</h1>
                    <p style="text-align: center; color: #666;">Application is running correctly. Use the following links to access API documentation:</p>
                    <div class="api-links">
                        <a href="/docs">Swagger UI Documentation</a>
                        <a href="/redoc">ReDoc Documentation</a>
                        <a href="/api/v1/health">Application Status</a>
                    </div>
                </div>
            </body>
            </html>
            """)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading main page: {str(e)}")


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint (legacy)."""
    uptime = time.time() - start_time
    return HealthCheck(
        status="healthy",
        version="1.0.0",
        uptime=uptime
    )


@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    try:
        # Create uploads directory
        upload_path = get_upload_path()
        print(f"Uploads directory created: {upload_path}")
        
        # Create static directory if it doesn't exist
        static_path = Path("static")
        static_path.mkdir(exist_ok=True)
        print(f"Static directory verified: {static_path}")
        
        print("Application started successfully")
        print(f"Documentation available at: http://{settings.HOST}:{settings.PORT}/docs")
        print(f"Frontend available at: http://{settings.HOST}:{settings.PORT}/")
        
    except Exception as e:
        print(f"Error during startup: {str(e)}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    print("Application closed")


# Custom error handler
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 error handler."""
    return HTMLResponse(
        content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>404 - Page Not Found</title>
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
                <p>The page you're looking for doesn't exist.</p>
                <p><a href="/">← Back to home</a></p>
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