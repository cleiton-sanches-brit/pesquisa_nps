-- ============================================================================
-- TABELA: respondents
-- Descrição: Cadastro de possíveis respondentes
-- Chave primária: id
-- Chave de conexão para Power BI: email
-- ============================================================================

CREATE TABLE IF NOT EXISTS respondents (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(254) NOT NULL UNIQUE,
    nome_conta VARCHAR(200),
    nome_usuario VARCHAR(200),
    status_usuario VARCHAR(50) DEFAULT 'Ativo',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    notes TEXT,
    active BOOLEAN DEFAULT TRUE NOT NULL
);

-- Índices
CREATE INDEX IF NOT EXISTS respondents_email_idx ON respondents(email);
CREATE INDEX IF NOT EXISTS respondents_status_idx ON respondents(status_usuario);
CREATE INDEX IF NOT EXISTS respondents_active_idx ON respondents(active);
CREATE INDEX IF NOT EXISTS respondents_created_at_idx ON respondents(created_at);

-- Comentários
COMMENT ON TABLE respondents IS 'Cadastro de possíveis respondentes - para Power BI';
COMMENT ON COLUMN respondents.email IS 'Chave de conexão: Email do usuário';
COMMENT ON COLUMN respondents.nome_conta IS 'Nome da conta/organização';
COMMENT ON COLUMN respondents.nome_usuario IS 'Nome completo do usuário';
COMMENT ON COLUMN respondents.status_usuario IS 'Status: Ativo, Inativo, Bloqueado, etc.';

-- Trigger para atualizar updated_at
CREATE OR REPLACE FUNCTION update_respondents_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_respondents_updated_at_trigger ON respondents;
CREATE TRIGGER update_respondents_updated_at_trigger
    BEFORE UPDATE ON respondents
    FOR EACH ROW
    EXECUTE FUNCTION update_respondents_updated_at();

-- Dados de exemplo (opcional - descomente se quiser dados de teste)
/*
INSERT INTO respondents (email, nome_conta, nome_usuario, status_usuario) VALUES
('usuario1@example.com', 'Empresa A', 'João Silva', 'Ativo'),
('usuario2@example.com', 'Empresa B', 'Maria Santos', 'Ativo'),
('usuario3@example.com', 'Empresa A', 'Pedro Costa', 'Inativo')
ON CONFLICT (email) DO NOTHING;
*/

-- Verificação
DO $$
BEGIN
    RAISE NOTICE 'Tabela respondents criada com sucesso!';
    RAISE NOTICE 'Colunas: id, email, nome_conta, nome_usuario, status_usuario, created_at, updated_at';
END $$;
