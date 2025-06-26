#!/usr/bin/env python3
"""
Script de prueba para verificar la descarga de archivos
"""

import os
import sys
from pathlib import Path

def test_file_access():
    """Prueba el acceso a los archivos en el directorio uploads"""
    
    # Obtener la ruta del directorio uploads
    upload_path = Path("uploads")
    
    print("🔍 Verificando acceso a archivos...")
    print(f"📁 Directorio uploads: {upload_path.absolute()}")
    print(f"📂 Existe: {upload_path.exists()}")
    
    if not upload_path.exists():
        print("❌ El directorio uploads no existe")
        return False
    
    # Buscar todos los archivos PDF
    pdf_files = []
    for root, dirs, files in os.walk(upload_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                file_path = Path(root) / file
                pdf_files.append(file_path)
    
    print(f"📄 Archivos PDF encontrados: {len(pdf_files)}")
    
    for file_path in pdf_files:
        print(f"\n📄 Archivo: {file_path}")
        print(f"   📂 Existe: {file_path.exists()}")
        print(f"   📂 Es archivo: {file_path.is_file()}")
        print(f"   📏 Tamaño: {file_path.stat().st_size} bytes")
        print(f"   🔐 Legible: {os.access(file_path, os.R_OK)}")
        
        # Calcular ruta relativa
        rel_path = file_path.relative_to(upload_path)
        print(f"   📍 Ruta relativa: {rel_path}")
        
        # Simular la ruta que usaría la API
        api_path = str(rel_path).replace('\\', '/')
        print(f"   🌐 Ruta API: {api_path}")
    
    return True

def test_api_endpoint():
    """Prueba el endpoint de la API"""
    import requests
    
    print("\n🌐 Probando endpoint de la API...")
    
    try:
        # Probar el endpoint de salud
        response = requests.get("http://localhost:8000/api/v1/health")
        print(f"✅ API respondiendo: {response.status_code}")
        
        # Listar directorios
        response = requests.get("http://localhost:8000/api/v1/directories")
        if response.status_code == 200:
            directories = response.json()
            print(f"📁 Directorios disponibles: {directories}")
            
            # Si hay directorios, listar archivos del primero
            if directories:
                first_dir = directories[0]
                print(f"📄 Listando archivos en: {first_dir}")
                response = requests.get(f"http://localhost:8000/api/v1/files/{first_dir}")
                if response.status_code == 200:
                    files = response.json()
                    print(f"📄 Archivos en {first_dir}: {files}")
                    
                    # Probar descarga del primer archivo
                    if files:
                        first_file = files[0]
                        file_path = first_file['path']
                        print(f"🔍 Probando descarga de: {file_path}")
                        
                        response = requests.head(f"http://localhost:8000/api/v1/files/download/{file_path}")
                        print(f"📥 Respuesta HEAD: {response.status_code}")
                        
                        if response.status_code == 200:
                            print("✅ El archivo está disponible para descarga")
                        else:
                            print(f"❌ Error en descarga: {response.status_code}")
                            print(f"   📝 Respuesta: {response.text}")
        
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar a la API. Asegúrate de que el servidor esté ejecutándose.")
    except Exception as e:
        print(f"❌ Error al probar la API: {str(e)}")

if __name__ == "__main__":
    print("🚀 Script de prueba para verificar descarga de archivos")
    print("=" * 60)
    
    # Verificar archivos locales
    test_file_access()
    
    # Verificar API
    test_api_endpoint()
    
    print("\n✅ Prueba completada") 