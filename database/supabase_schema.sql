-- ============================================================================
-- SCRIPT DE CRIAÇÃO DE TABELAS PARA SUPABASE POSTGRESQL
-- Sistema de Pesquisas NPS
-- ============================================================================
-- 
-- INSTRUÇÕES:
-- 1. Acesse o Supabase Dashboard
-- 2. Vá em SQL Editor
-- 3. Cole este script completo
-- 4. Execute o script
-- 
-- NOTA: Este script cria apenas as tabelas do app 'surveys'
-- As tabelas do Django (auth_user, etc.) serão criadas automaticamente
-- quando você executar as migrações do Django conectado ao Supabase
-- ============================================================================

-- Habilitar extensão UUID se não estiver habilitada
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- TABELA: surveys_survey
-- Descrição: Armazena as pesquisas NPS
-- ============================================================================
CREATE TABLE IF NOT EXISTS surveys_survey (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_by_id INTEGER NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE,
    allow_multiple_responses BOOLEAN DEFAULT FALSE NOT NULL
);

-- Índices para surveys_survey
CREATE INDEX IF NOT EXISTS surveys_survey_created_by_id_idx ON surveys_survey(created_by_id);
CREATE INDEX IF NOT EXISTS surveys_survey_created_at_idx ON surveys_survey(created_at DESC);
CREATE INDEX IF NOT EXISTS surveys_survey_is_active_idx ON surveys_survey(is_active);

-- Comentários na tabela
COMMENT ON TABLE surveys_survey IS 'Armazena as pesquisas NPS';
COMMENT ON COLUMN surveys_survey.title IS 'Título da pesquisa';
COMMENT ON COLUMN surveys_survey.description IS 'Descrição detalhada da pesquisa';
COMMENT ON COLUMN surveys_survey.is_active IS 'Indica se a pesquisa está ativa';
COMMENT ON COLUMN surveys_survey.expires_at IS 'Data e hora de expiração da pesquisa';
COMMENT ON COLUMN surveys_survey.allow_multiple_responses IS 'Permite múltiplas respostas do mesmo respondente';

-- ============================================================================
-- TABELA: surveys_surveyinvitation
-- Descrição: Armazena convites únicos por email para pesquisas
-- ============================================================================
CREATE TABLE IF NOT EXISTS surveys_surveyinvitation (
    id BIGSERIAL PRIMARY KEY,
    survey_id BIGINT NOT NULL,
    email VARCHAR(254) NOT NULL,
    unique_token UUID DEFAULT uuid_generate_v4() NOT NULL UNIQUE,
    is_used BOOLEAN DEFAULT FALSE NOT NULL,
    used_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT surveys_surveyinvitation_survey_email_unique UNIQUE (survey_id, email)
);

-- Índices para surveys_surveyinvitation
CREATE INDEX IF NOT EXISTS surveys_surveyinvitation_survey_id_idx ON surveys_surveyinvitation(survey_id);
CREATE INDEX IF NOT EXISTS surveys_surveyinvitation_email_idx ON surveys_surveyinvitation(email);
CREATE INDEX IF NOT EXISTS surveys_surveyinvitation_unique_token_idx ON surveys_surveyinvitation(unique_token);
CREATE INDEX IF NOT EXISTS surveys_surveyinvitation_is_used_idx ON surveys_surveyinvitation(is_used);
CREATE INDEX IF NOT EXISTS surveys_surveyinvitation_expires_at_idx ON surveys_surveyinvitation(expires_at);
CREATE INDEX IF NOT EXISTS surveys_surveyinvitation_created_at_idx ON surveys_surveyinvitation(created_at DESC);

-- Comentários na tabela
COMMENT ON TABLE surveys_surveyinvitation IS 'Convites únicos por email para pesquisas';
COMMENT ON COLUMN surveys_surveyinvitation.unique_token IS 'Token UUID único para cada convite';
COMMENT ON COLUMN surveys_surveyinvitation.is_used IS 'Indica se o convite já foi utilizado';
COMMENT ON COLUMN surveys_surveyinvitation.expires_at IS 'Data e hora de expiração do convite';

-- ============================================================================
-- TABELA: surveys_question
-- Descrição: Armazena as perguntas de uma pesquisa
-- ============================================================================
CREATE TABLE IF NOT EXISTS surveys_question (
    id BIGSERIAL PRIMARY KEY,
    survey_id BIGINT NOT NULL,
    question_text TEXT NOT NULL,
    question_type VARCHAR(10) NOT NULL CHECK (question_type IN ('nps', 'text', 'choice', 'rating')),
    is_required BOOLEAN DEFAULT TRUE NOT NULL,
    "order" INTEGER DEFAULT 0 NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Índices para surveys_question
CREATE INDEX IF NOT EXISTS surveys_question_survey_id_idx ON surveys_question(survey_id);
CREATE INDEX IF NOT EXISTS surveys_question_order_idx ON surveys_question("order", created_at);
CREATE INDEX IF NOT EXISTS surveys_question_question_type_idx ON surveys_question(question_type);

-- Comentários na tabela
COMMENT ON TABLE surveys_question IS 'Perguntas de uma pesquisa';
COMMENT ON COLUMN surveys_question.question_type IS 'Tipo: nps, text, choice, rating';
COMMENT ON COLUMN surveys_question."order" IS 'Ordem de exibição da pergunta';

-- ============================================================================
-- TABELA: surveys_choice
-- Descrição: Opções de múltipla escolha para perguntas
-- ============================================================================
CREATE TABLE IF NOT EXISTS surveys_choice (
    id BIGSERIAL PRIMARY KEY,
    question_id BIGINT NOT NULL,
    choice_text VARCHAR(200) NOT NULL,
    value VARCHAR(50) NOT NULL,
    "order" INTEGER DEFAULT 0 NOT NULL
);

-- Índices para surveys_choice
CREATE INDEX IF NOT EXISTS surveys_choice_question_id_idx ON surveys_choice(question_id);
CREATE INDEX IF NOT EXISTS surveys_choice_order_idx ON surveys_choice("order");

-- Comentários na tabela
COMMENT ON TABLE surveys_choice IS 'Opções de múltipla escolha para perguntas';
COMMENT ON COLUMN surveys_choice."order" IS 'Ordem de exibição da opção';

-- ============================================================================
-- TABELA: surveys_surveyresponse
-- Descrição: Armazena respostas completas de pesquisas
-- ============================================================================
CREATE TABLE IF NOT EXISTS surveys_surveyresponse (
    id BIGSERIAL PRIMARY KEY,
    survey_id BIGINT NOT NULL,
    invitation_id BIGINT,
    respondent_id VARCHAR(100) NOT NULL,
    respondent_email VARCHAR(254),
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ip_address INET,
    user_agent TEXT,
    CONSTRAINT surveys_surveyresponse_survey_respondent_unique UNIQUE (survey_id, respondent_id)
);

-- Índices para surveys_surveyresponse
CREATE INDEX IF NOT EXISTS surveys_surveyresponse_survey_id_idx ON surveys_surveyresponse(survey_id);
CREATE INDEX IF NOT EXISTS surveys_surveyresponse_invitation_id_idx ON surveys_surveyresponse(invitation_id);
CREATE INDEX IF NOT EXISTS surveys_surveyresponse_respondent_id_idx ON surveys_surveyresponse(respondent_id);
CREATE INDEX IF NOT EXISTS surveys_surveyresponse_respondent_email_idx ON surveys_surveyresponse(respondent_email);
CREATE INDEX IF NOT EXISTS surveys_surveyresponse_submitted_at_idx ON surveys_surveyresponse(submitted_at DESC);

-- Comentários na tabela
COMMENT ON TABLE surveys_surveyresponse IS 'Respostas completas de pesquisas';
COMMENT ON COLUMN surveys_surveyresponse.invitation_id IS 'Referência ao convite (se aplicável)';
COMMENT ON COLUMN surveys_surveyresponse.ip_address IS 'Endereço IP do respondente';
COMMENT ON COLUMN surveys_surveyresponse.user_agent IS 'User Agent do navegador';

-- ============================================================================
-- TABELA: surveys_answer
-- Descrição: Armazena respostas individuais a perguntas
-- ============================================================================
CREATE TABLE IF NOT EXISTS surveys_answer (
    id BIGSERIAL PRIMARY KEY,
    response_id BIGINT NOT NULL,
    question_id BIGINT NOT NULL,
    answer_text TEXT,
    answer_value VARCHAR(100),
    answer_choice_id BIGINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT surveys_answer_response_question_unique UNIQUE (response_id, question_id)
);

-- Índices para surveys_answer
CREATE INDEX IF NOT EXISTS surveys_answer_response_id_idx ON surveys_answer(response_id);
CREATE INDEX IF NOT EXISTS surveys_answer_question_id_idx ON surveys_answer(question_id);
CREATE INDEX IF NOT EXISTS surveys_answer_answer_choice_id_idx ON surveys_answer(answer_choice_id);

-- Comentários na tabela
COMMENT ON TABLE surveys_answer IS 'Respostas individuais a perguntas';
COMMENT ON COLUMN surveys_answer.answer_text IS 'Resposta em texto livre';
COMMENT ON COLUMN surveys_answer.answer_value IS 'Valor da resposta (para NPS, rating, etc.)';
COMMENT ON COLUMN surveys_answer.answer_choice_id IS 'Referência à opção escolhida (para múltipla escolha)';

-- ============================================================================
-- TABELA: surveys_npsresult
-- Descrição: Armazena resultados calculados de NPS
-- ============================================================================
CREATE TABLE IF NOT EXISTS surveys_npsresult (
    id BIGSERIAL PRIMARY KEY,
    survey_id BIGINT NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    total_responses INTEGER NOT NULL,
    promoters INTEGER NOT NULL,
    passives INTEGER NOT NULL,
    detractors INTEGER NOT NULL,
    nps_score NUMERIC(5,2) NOT NULL,
    calculated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT surveys_npsresult_survey_period_unique UNIQUE (survey_id, period_start, period_end)
);

-- Índices para surveys_npsresult
CREATE INDEX IF NOT EXISTS surveys_npsresult_survey_id_idx ON surveys_npsresult(survey_id);
CREATE INDEX IF NOT EXISTS surveys_npsresult_calculated_at_idx ON surveys_npsresult(calculated_at DESC);
CREATE INDEX IF NOT EXISTS surveys_npsresult_period_idx ON surveys_npsresult(period_start, period_end);

-- Comentários na tabela
COMMENT ON TABLE surveys_npsresult IS 'Resultados calculados de NPS por período';
COMMENT ON COLUMN surveys_npsresult.promoters IS 'Quantidade de promotores (9-10)';
COMMENT ON COLUMN surveys_npsresult.passives IS 'Quantidade de neutros (7-8)';
COMMENT ON COLUMN surveys_npsresult.detractors IS 'Quantidade de detratores (0-6)';
COMMENT ON COLUMN surveys_npsresult.nps_score IS 'Score NPS calculado';

-- ============================================================================
-- FOREIGN KEYS (Chaves Estrangeiras)
-- ============================================================================

-- surveys_survey -> auth_user
ALTER TABLE surveys_survey
    ADD CONSTRAINT surveys_survey_created_by_id_fk
    FOREIGN KEY (created_by_id)
    REFERENCES auth_user(id)
    ON DELETE CASCADE;

-- surveys_surveyinvitation -> surveys_survey
ALTER TABLE surveys_surveyinvitation
    ADD CONSTRAINT surveys_surveyinvitation_survey_id_fk
    FOREIGN KEY (survey_id)
    REFERENCES surveys_survey(id)
    ON DELETE CASCADE;

-- surveys_question -> surveys_survey
ALTER TABLE surveys_question
    ADD CONSTRAINT surveys_question_survey_id_fk
    FOREIGN KEY (survey_id)
    REFERENCES surveys_survey(id)
    ON DELETE CASCADE;

-- surveys_choice -> surveys_question
ALTER TABLE surveys_choice
    ADD CONSTRAINT surveys_choice_question_id_fk
    FOREIGN KEY (question_id)
    REFERENCES surveys_question(id)
    ON DELETE CASCADE;

-- surveys_surveyresponse -> surveys_survey
ALTER TABLE surveys_surveyresponse
    ADD CONSTRAINT surveys_surveyresponse_survey_id_fk
    FOREIGN KEY (survey_id)
    REFERENCES surveys_survey(id)
    ON DELETE CASCADE;

-- surveys_surveyresponse -> surveys_surveyinvitation
ALTER TABLE surveys_surveyresponse
    ADD CONSTRAINT surveys_surveyresponse_invitation_id_fk
    FOREIGN KEY (invitation_id)
    REFERENCES surveys_surveyinvitation(id)
    ON DELETE CASCADE;

-- surveys_answer -> surveys_surveyresponse
ALTER TABLE surveys_answer
    ADD CONSTRAINT surveys_answer_response_id_fk
    FOREIGN KEY (response_id)
    REFERENCES surveys_surveyresponse(id)
    ON DELETE CASCADE;

-- surveys_answer -> surveys_question
ALTER TABLE surveys_answer
    ADD CONSTRAINT surveys_answer_question_id_fk
    FOREIGN KEY (question_id)
    REFERENCES surveys_question(id)
    ON DELETE CASCADE;

-- surveys_answer -> surveys_choice
ALTER TABLE surveys_answer
    ADD CONSTRAINT surveys_answer_answer_choice_id_fk
    FOREIGN KEY (answer_choice_id)
    REFERENCES surveys_choice(id)
    ON DELETE CASCADE;

-- surveys_npsresult -> surveys_survey
ALTER TABLE surveys_npsresult
    ADD CONSTRAINT surveys_npsresult_survey_id_fk
    FOREIGN KEY (survey_id)
    REFERENCES surveys_survey(id)
    ON DELETE CASCADE;

-- ============================================================================
-- FUNÇÕES ÚTEIS (Opcional - podem ser úteis para consultas)
-- ============================================================================

-- Função para verificar se um convite é válido
CREATE OR REPLACE FUNCTION is_invitation_valid(invitation_token UUID)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 
        FROM surveys_surveyinvitation 
        WHERE unique_token = invitation_token
        AND is_used = FALSE
        AND expires_at > CURRENT_TIMESTAMP
    );
END;
$$ LANGUAGE plpgsql;

-- Função para calcular NPS score
CREATE OR REPLACE FUNCTION calculate_nps_score(
    p_promoters INTEGER,
    p_passives INTEGER,
    p_detractors INTEGER,
    p_total INTEGER
)
RETURNS NUMERIC(5,2) AS $$
BEGIN
    IF p_total = 0 THEN
        RETURN 0;
    END IF;
    
    RETURN ROUND(
        ((p_promoters::NUMERIC / p_total::NUMERIC) - 
         (p_detractors::NUMERIC / p_total::NUMERIC)) * 100,
        2
    );
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- TRIGGERS (Opcional - atualização automática de updated_at)
-- ============================================================================

-- Trigger para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger na tabela surveys_survey
CREATE TRIGGER update_surveys_survey_updated_at
    BEFORE UPDATE ON surveys_survey
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- SEQUENCES (Verificar se as sequences estão configuradas)
-- ============================================================================

-- As sequences são criadas automaticamente com BIGSERIAL
-- Mas podemos verificar se existem:

DO $$
BEGIN
    -- Verificar e criar sequences se necessário
    IF NOT EXISTS (SELECT 1 FROM pg_sequences WHERE sequencename = 'surveys_survey_id_seq') THEN
        CREATE SEQUENCE surveys_survey_id_seq;
    END IF;
    -- ... outras sequences são criadas automaticamente
END $$;

-- ============================================================================
-- PERMISSÕES (Ajustar conforme necessário)
-- ============================================================================

-- Dar permissões ao usuário anônimo do Supabase (se necessário)
-- GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO anon;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO anon;

-- Dar permissões ao usuário autenticado do Supabase (se necessário)
-- GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO authenticated;

-- ============================================================================
-- VALIDAÇÕES E DADOS INICIAIS (Opcional)
-- ============================================================================

-- Podemos adicionar dados de exemplo aqui se necessário
-- (Não incluído por padrão para manter o banco limpo)

-- ============================================================================
-- VERIFICAÇÃO FINAL
-- ============================================================================

-- Verificar se todas as tabelas foram criadas
DO $$
DECLARE
    table_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO table_count
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_name LIKE 'surveys_%';
    
    RAISE NOTICE 'Total de tabelas surveys criadas: %', table_count;
    
    IF table_count < 7 THEN
        RAISE WARNING 'Algumas tabelas podem não ter sido criadas. Verifique os erros acima.';
    ELSE
        RAISE NOTICE 'Todas as tabelas foram criadas com sucesso!';
    END IF;
END $$;

-- ============================================================================
-- FIM DO SCRIPT
-- ============================================================================
