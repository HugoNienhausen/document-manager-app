-- =====================================================
-- Esquema de Base de Datos para PDF Manager
-- PostgreSQL
-- =====================================================

-- Crear la base de datos (ejecutar como superusuario)
-- CREATE DATABASE pdf_manager;

-- Conectar a la base de datos
-- \c pdf_manager;

-- =====================================================
-- Tabla: document_types (Tipos de documentos)
-- =====================================================
CREATE TABLE IF NOT EXISTS document_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    icon VARCHAR(50) DEFAULT 'fas fa-file-pdf',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para document_types
CREATE INDEX IF NOT EXISTS idx_document_types_name ON document_types(name);
CREATE INDEX IF NOT EXISTS idx_document_types_active ON document_types(is_active);

-- =====================================================
-- Tabla: clients (Clientes)
-- =====================================================
CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para clients
CREATE INDEX IF NOT EXISTS idx_clients_name ON clients(name);
CREATE INDEX IF NOT EXISTS idx_clients_email ON clients(email);
CREATE INDEX IF NOT EXISTS idx_clients_active ON clients(is_active);

-- =====================================================
-- Tabla: categories (Categorías)
-- =====================================================
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    color VARCHAR(7) DEFAULT '#3b82f6',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para categories
CREATE INDEX IF NOT EXISTS idx_categories_name ON categories(name);
CREATE INDEX IF NOT EXISTS idx_categories_active ON categories(is_active);

-- =====================================================
-- Tabla: documents (Documentos)
-- =====================================================
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_hash VARCHAR(64) NOT NULL UNIQUE,
    document_type_id INTEGER NOT NULL,
    client_id INTEGER,
    category_id INTEGER NOT NULL,
    local_path VARCHAR(500) NOT NULL,
    extracted_text TEXT,
    file_size INTEGER NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Claves foráneas
    FOREIGN KEY (document_type_id) REFERENCES document_types(id) ON DELETE RESTRICT,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE SET NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT
);

-- Índices para documents
CREATE INDEX IF NOT EXISTS idx_documents_filename ON documents(filename);
CREATE INDEX IF NOT EXISTS idx_documents_file_hash ON documents(file_hash);
CREATE INDEX IF NOT EXISTS idx_documents_document_type_id ON documents(document_type_id);
CREATE INDEX IF NOT EXISTS idx_documents_client_id ON documents(client_id);
CREATE INDEX IF NOT EXISTS idx_documents_category_id ON documents(category_id);
CREATE INDEX IF NOT EXISTS idx_documents_upload_date ON documents(upload_date);
CREATE INDEX IF NOT EXISTS idx_documents_active ON documents(is_active);
CREATE INDEX IF NOT EXISTS idx_documents_created_at ON documents(created_at);

-- Índice compuesto para búsquedas eficientes
CREATE INDEX IF NOT EXISTS idx_documents_search ON documents(filename, document_type_id, category_id, is_active);

-- =====================================================
-- Datos iniciales
-- =====================================================

-- Insertar tipos de documentos por defecto
INSERT INTO document_types (name, description, icon) VALUES
('Factura', 'Documentos de facturación', 'fas fa-file-invoice'),
('Contrato', 'Contratos y acuerdos', 'fas fa-file-contract'),
('Recibo', 'Recibos de pago', 'fas fa-receipt'),
('Identificación', 'Documentos de identificación', 'fas fa-id-card'),
('Certificado', 'Certificados oficiales', 'fas fa-certificate'),
('Otro', 'Otros tipos de documentos', 'fas fa-file-pdf')
ON CONFLICT (name) DO NOTHING;

-- Insertar categorías por defecto
INSERT INTO categories (name, description, color) VALUES
('Financiero', 'Documentos relacionados con finanzas', '#10b981'),
('Legal', 'Documentos legales y contratos', '#3b82f6'),
('Personal', 'Documentos personales', '#f59e0b'),
('Laboral', 'Documentos relacionados con trabajo', '#8b5cf6'),
('Médico', 'Documentos médicos', '#ef4444'),
('Otros', 'Otras categorías', '#6b7280')
ON CONFLICT (name) DO NOTHING;

-- =====================================================
-- Funciones y triggers
-- =====================================================

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para actualizar updated_at
CREATE TRIGGER update_document_types_updated_at 
    BEFORE UPDATE ON document_types 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_clients_updated_at 
    BEFORE UPDATE ON clients 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_categories_updated_at 
    BEFORE UPDATE ON categories 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_documents_updated_at 
    BEFORE UPDATE ON documents 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- Vistas útiles
-- =====================================================

-- Vista para documentos con información completa
CREATE OR REPLACE VIEW documents_view AS
SELECT 
    d.id,
    d.filename,
    d.file_hash,
    d.local_path,
    d.extracted_text,
    d.file_size,
    d.upload_date,
    d.is_active,
    d.created_at,
    d.updated_at,
    dt.name as document_type_name,
    dt.icon as document_type_icon,
    c.name as client_name,
    c.email as client_email,
    cat.name as category_name,
    cat.color as category_color
FROM documents d
LEFT JOIN document_types dt ON d.document_type_id = dt.id
LEFT JOIN clients c ON d.client_id = c.id
LEFT JOIN categories cat ON d.category_id = cat.id
WHERE d.is_active = TRUE;

-- Vista para estadísticas
CREATE OR REPLACE VIEW document_stats AS
SELECT 
    COUNT(*) as total_documents,
    COUNT(DISTINCT client_id) as total_clients,
    COUNT(DISTINCT category_id) as total_categories,
    SUM(file_size) as total_size_bytes,
    AVG(file_size) as avg_file_size,
    MIN(upload_date) as oldest_document,
    MAX(upload_date) as newest_document
FROM documents
WHERE is_active = TRUE;

-- =====================================================
-- Comentarios
-- =====================================================

COMMENT ON TABLE document_types IS 'Tipos de documentos disponibles en el sistema';
COMMENT ON TABLE clients IS 'Clientes asociados a los documentos';
COMMENT ON TABLE categories IS 'Categorías para organizar documentos';
COMMENT ON TABLE documents IS 'Documentos almacenados en el sistema';

COMMENT ON COLUMN documents.file_hash IS 'Hash SHA-256 del archivo para evitar duplicados';
COMMENT ON COLUMN documents.local_path IS 'Ruta local donde se almacena el archivo físico';
COMMENT ON COLUMN documents.extracted_text IS 'Texto extraído del PDF para búsquedas';
COMMENT ON COLUMN documents.file_size IS 'Tamaño del archivo en bytes'; 