#!/bin/bash

# Script para configurar PostgreSQL para PDF Manager
# =================================================

echo "🚀 Configurando PostgreSQL para PDF Manager..."

# Verificar si PostgreSQL está instalado
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL no está instalado."
    echo "📦 Instalando PostgreSQL..."
    
    # Detectar el sistema operativo
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install postgresql
            brew services start postgresql
        else
            echo "❌ Homebrew no está instalado. Instala PostgreSQL manualmente."
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y postgresql postgresql-contrib
            sudo systemctl start postgresql
            sudo systemctl enable postgresql
        elif command -v yum &> /dev/null; then
            sudo yum install -y postgresql postgresql-server
            sudo postgresql-setup initdb
            sudo systemctl start postgresql
            sudo systemctl enable postgresql
        else
            echo "❌ No se pudo detectar el gestor de paquetes. Instala PostgreSQL manualmente."
            exit 1
        fi
    else
        echo "❌ Sistema operativo no soportado. Instala PostgreSQL manualmente."
        exit 1
    fi
fi

echo "✅ PostgreSQL está instalado y ejecutándose."

# Crear la base de datos
echo "📊 Creando base de datos 'pdf_manager'..."

# Intentar crear la base de datos
if psql -U postgres -c "CREATE DATABASE pdf_manager;" 2>/dev/null; then
    echo "✅ Base de datos 'pdf_manager' creada exitosamente."
else
    echo "ℹ️  La base de datos 'pdf_manager' ya existe o hay un problema de permisos."
fi

# Crear usuario si no existe
echo "👤 Creando usuario 'pdf_user'..."
if psql -U postgres -c "CREATE USER pdf_user WITH PASSWORD 'password';" 2>/dev/null; then
    echo "✅ Usuario 'pdf_user' creado exitosamente."
else
    echo "ℹ️  El usuario 'pdf_user' ya existe."
fi

# Otorgar permisos
echo "🔐 Otorgando permisos..."
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE pdf_manager TO pdf_user;" 2>/dev/null
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE pdf_manager TO postgres;" 2>/dev/null

echo "✅ Permisos otorgados."

# Ejecutar el esquema SQL
echo "📋 Ejecutando esquema de base de datos..."
if psql -U postgres -d pdf_manager -f database_schema.sql; then
    echo "✅ Esquema de base de datos ejecutado exitosamente."
else
    echo "❌ Error al ejecutar el esquema de base de datos."
    exit 1
fi

echo ""
echo "🎉 Configuración de PostgreSQL completada!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Copia config.env a .env y ajusta las credenciales si es necesario"
echo "2. Ejecuta: python scripts/init_database.py"
echo "3. Inicia la aplicación: python main.py"
echo ""
echo "🔗 URLs de la aplicación:"
echo "   - Frontend: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - ReDoc: http://localhost:8000/redoc" 