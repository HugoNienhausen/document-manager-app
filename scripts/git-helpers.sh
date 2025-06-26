#!/bin/bash

# Scripts de ayuda para Git y control de versiones
# Uso: source scripts/git-helpers.sh

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar el estado actual del repositorio
function git_status() {
    echo -e "${BLUE}📊 Estado actual del repositorio:${NC}"
    echo "----------------------------------------"
    git status --short
    echo ""
    echo -e "${BLUE}📝 Últimos commits:${NC}"
    echo "----------------------------------------"
    git log --oneline -5
    echo ""
}

# Función para hacer commit con mensaje estructurado
function git_commit() {
    if [ $# -eq 0 ]; then
        echo -e "${RED}❌ Error: Debes proporcionar un mensaje de commit${NC}"
        echo "Uso: git_commit 'tipo: descripción del cambio'"
        echo "Tipos: feat, fix, docs, style, refactor, test, chore"
        return 1
    fi
    
    local message="$1"
    local current_date=$(date +"%d/%m/%Y")
    
    echo -e "${BLUE}🔄 Preparando commit...${NC}"
    
    # Añadir todos los cambios
    git add .
    
    # Hacer commit
    git commit -m "$message"
    
    echo -e "${GREEN}✅ Commit realizado exitosamente${NC}"
    echo -e "${YELLOW}💡 Próximos pasos recomendados:${NC}"
    echo "1. Revisar el commit: git log --oneline -1"
    echo "2. Actualizar CHANGELOG.md si es necesario"
    echo "3. Crear tag si es una nueva versión: git tag v1.x.x"
}

# Función para actualizar el CHANGELOG automáticamente
function update_changelog() {
    local version="$1"
    local change_type="$2"
    local description="$3"
    
    if [ $# -lt 3 ]; then
        echo -e "${RED}❌ Error: Debes proporcionar versión, tipo y descripción${NC}"
        echo "Uso: update_changelog '1.1.0' 'Mejorado' 'Descripción del cambio'"
        return 1
    fi
    
    local current_date=$(date +"%d/%m/%Y")
    local changelog_file="CHANGELOG.md"
    
    # Crear la entrada del changelog
    local entry="## [$version] - $current_date

### $change_type
- $description

---"
    
    # Insertar después de la línea del changelog
    sed -i.bak "3a\\
$entry
" "$changelog_file"
    
    # Limpiar archivo de backup
    rm "${changelog_file}.bak"
    
    echo -e "${GREEN}✅ CHANGELOG actualizado${NC}"
}

# Función para crear una nueva versión
function create_version() {
    local version="$1"
    local message="$2"
    
    if [ $# -lt 2 ]; then
        echo -e "${RED}❌ Error: Debes proporcionar versión y mensaje${NC}"
        echo "Uso: create_version '1.1.0' 'Nueva funcionalidad X'"
        return 1
    fi
    
    echo -e "${BLUE}🏷️  Creando versión $version...${NC}"
    
    # Crear tag
    git tag -a "v$version" -m "$message"
    
    echo -e "${GREEN}✅ Versión v$version creada${NC}"
    echo -e "${YELLOW}💡 Para subir al repositorio remoto:${NC}"
    echo "git push origin master --tags"
}

# Función para hacer commit completo con changelog
function smart_commit() {
    local commit_type="$1"
    local description="$2"
    local version="$3"
    
    if [ $# -lt 2 ]; then
        echo -e "${RED}❌ Error: Debes proporcionar tipo y descripción${NC}"
        echo "Uso: smart_commit 'feat' 'nueva funcionalidad' [version]"
        return 1
    fi
    
    local commit_message="$commit_type: $description"
    
    echo -e "${BLUE}🚀 Iniciando commit inteligente...${NC}"
    
    # Hacer commit
    git_commit "$commit_message"
    
    # Si se proporciona versión, actualizar changelog
    if [ ! -z "$version" ]; then
        echo -e "${BLUE}📝 Actualizando CHANGELOG...${NC}"
        update_changelog "$version" "Añadido" "$description"
        
        # Hacer commit del changelog
        git add CHANGELOG.md
        git commit -m "docs: actualizar CHANGELOG para v$version"
        
        # Crear tag de versión
        create_version "$version" "$description"
    fi
    
    echo -e "${GREEN}✅ Proceso completado${NC}"
}

# Función para mostrar ayuda
function git_help() {
    echo -e "${BLUE}🛠️  Scripts de ayuda para Git${NC}"
    echo "=================================="
    echo ""
    echo -e "${YELLOW}Comandos disponibles:${NC}"
    echo ""
    echo -e "${GREEN}git_status${NC} - Mostrar estado del repositorio"
    echo -e "${GREEN}git_commit 'mensaje'${NC} - Hacer commit con mensaje"
    echo -e "${GREEN}update_changelog 'v1.1.0' 'Mejorado' 'descripción'${NC} - Actualizar CHANGELOG"
    echo -e "${GREEN}create_version '1.1.0' 'mensaje'${NC} - Crear nueva versión"
    echo -e "${GREEN}smart_commit 'feat' 'descripción' [version]${NC} - Commit completo"
    echo ""
    echo -e "${YELLOW}Tipos de commit:${NC}"
    echo "feat: nueva funcionalidad"
    echo "fix: corrección de bug"
    echo "docs: documentación"
    echo "style: cambios de estilo"
    echo "refactor: refactorización"
    echo "test: pruebas"
    echo "chore: tareas de mantenimiento"
    echo ""
    echo -e "${YELLOW}Ejemplos de uso:${NC}"
    echo "smart_commit 'feat' 'añadir funcionalidad de búsqueda' '1.2.0'"
    echo "git_commit 'fix: corregir error en subida de archivos'"
    echo "update_changelog '1.1.1' 'Corregido' 'error en navegación'"
}

# Función para checklist de commit
function commit_checklist() {
    echo -e "${BLUE}📋 Checklist para commits${NC}"
    echo "================================"
    echo ""
    echo -e "${YELLOW}Antes del commit:${NC}"
    echo "✅ ¿El código funciona correctamente?"
    echo "✅ ¿Has probado la funcionalidad?"
    echo "✅ ¿No hay errores de linting?"
    echo "✅ ¿Los cambios son coherentes?"
    echo ""
    echo -e "${YELLOW}Durante el commit:${NC}"
    echo "✅ ¿Mensaje descriptivo y claro?"
    echo "✅ ¿Tipo de commit correcto?"
    echo "✅ ¿Solo archivos relevantes incluidos?"
    echo ""
    echo -e "${YELLOW}Después del commit:${NC}"
    echo "✅ ¿Actualizar CHANGELOG.md si es necesario?"
    echo "✅ ¿Crear tag si es nueva versión?"
    echo "✅ ¿Probar en otro entorno?"
    echo "✅ ¿Documentar cambios importantes?"
    echo ""
    echo -e "${YELLOW}Para nuevas versiones:${NC}"
    echo "✅ ¿Incrementar versión en CHANGELOG?"
    echo "✅ ¿Crear tag con git tag v1.x.x?"
    echo "✅ ¿Actualizar README si es necesario?"
    echo "✅ ¿Hacer push con tags?"
}

# Mostrar ayuda al cargar el script
echo -e "${GREEN}✅ Scripts de Git cargados${NC}"
echo -e "${BLUE}💡 Usa 'git_help' para ver todos los comandos${NC}"
echo -e "${BLUE}📋 Usa 'commit_checklist' para ver el checklist${NC}" 