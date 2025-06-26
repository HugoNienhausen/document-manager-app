#!/bin/bash

# Script de ayuda para control de versiones
# Gestor de PDFs - Git Helpers

echo "🚀 Gestor de PDFs - Git Helpers"
echo "================================"
echo ""

# Función para mostrar el estado actual
show_status() {
    echo "📊 Estado actual del repositorio:"
    git status --short
    echo ""
}

# Función para hacer commit rápido
quick_commit() {
    if [ -z "$1" ]; then
        echo "❌ Error: Debes proporcionar un mensaje de commit"
        echo "Uso: ./git-helpers.sh commit 'Mensaje del commit'"
        exit 1
    fi
    
    echo "📝 Haciendo commit con mensaje: $1"
    git add .
    git commit -m "$1"
    echo "✅ Commit realizado exitosamente"
}

# Función para crear una nueva versión
new_version() {
    if [ -z "$1" ]; then
        echo "❌ Error: Debes proporcionar la nueva versión"
        echo "Uso: ./git-helpers.sh version 1.1.0"
        exit 1
    fi
    
    echo "🏷️  Creando nueva versión: $1"
    git tag -a "v$1" -m "Versión $1"
    echo "✅ Tag creado: v$1"
    echo "💡 Para subir el tag: git push origin v$1"
}

# Función para mostrar el historial
show_history() {
    echo "📜 Historial de commits:"
    git log --oneline --graph --decorate -10
    echo ""
}

# Función para limpiar branches
cleanup_branches() {
    echo "🧹 Limpiando branches locales..."
    git branch --merged | grep -v '\*\|master\|main' | xargs -n 1 git branch -d
    echo "✅ Limpieza completada"
}

# Función para mostrar ayuda
show_help() {
    echo "Comandos disponibles:"
    echo "  status                    - Mostrar estado del repositorio"
    echo "  commit 'mensaje'          - Hacer commit rápido"
    echo "  version '1.1.0'           - Crear nueva versión (tag)"
    echo "  history                   - Mostrar historial de commits"
    echo "  cleanup                   - Limpiar branches locales"
    echo "  help                      - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  ./git-helpers.sh commit 'Añadir nueva funcionalidad'"
    echo "  ./git-helpers.sh version 1.1.0"
    echo "  ./git-helpers.sh status"
}

# Procesar argumentos
case "$1" in
    "status")
        show_status
        ;;
    "commit")
        quick_commit "$2"
        ;;
    "version")
        new_version "$2"
        ;;
    "history")
        show_history
        ;;
    "cleanup")
        cleanup_branches
        ;;
    "help"|"")
        show_help
        ;;
    *)
        echo "❌ Comando no reconocido: $1"
        echo "Usa './git-helpers.sh help' para ver los comandos disponibles"
        exit 1
        ;;
esac 