-- ============================================================================
-- VIEWS PARA POWER BI - SISTEMA NPS SURVEYS
-- ============================================================================
-- 
-- Este script cria views otimizadas para consumo no Power BI
-- Chave de conexão: EMAIL (respondent_email)
-- 
-- Views criadas:
-- 1. vw_powerbi_respostas - Dados das respostas recebidas
-- 2. vw_powerbi_envios - Dados de envio de convites
-- 3. vw_powerbi_respondentes - Cadastro de possíveis respondentes
-- ============================================================================

-- ============================================================================
-- VIEW 1: vw_powerbi_respostas
-- Descrição: Tabela com dados das respostas recebidas
-- Chave: respondent_email (email do respondente)
-- ============================================================================
CREATE OR REPLACE VIEW vw_powerbi_respostas AS
SELECT 
    sr.id AS resposta_id,
    sr.respondent_email AS email_respondente,
    sr.respondent_id AS id_respondente,
    sr.survey_id AS pesquisa_id,
    s.title AS titulo_pesquisa,
    sr.submitted_at AS data_resposta,
    DATE(sr.submitted_at) AS data_resposta_date,
    EXTRACT(YEAR FROM sr.submitted_at) AS ano_resposta,
    EXTRACT(MONTH FROM sr.submitted_at) AS mes_resposta,
    EXTRACT(DAY FROM sr.submitted_at) AS dia_resposta,
    TO_CHAR(sr.submitted_at, 'YYYY-MM') AS ano_mes_resposta,
    sr.ip_address AS ip_respondente,
    sr.user_agent AS user_agent,
    sr.invitation_id AS convite_id,
    si.is_used AS convite_utilizado,
    si.created_at AS data_envio_convite,
    -- Respostas NPS (se existir pergunta NPS)
    (SELECT a.answer_value 
     FROM surveys_answer a
     JOIN surveys_question q ON a.question_id = q.id
     WHERE a.response_id = sr.id 
     AND q.question_type = 'nps'
     LIMIT 1) AS resposta_nps,
    -- Classificação NPS
    CASE 
        WHEN (SELECT a.answer_value 
              FROM surveys_answer a
              JOIN surveys_question q ON a.question_id = q.id
              WHERE a.response_id = sr.id 
              AND q.question_type = 'nps'
              LIMIT 1)::INTEGER >= 9 THEN 'Promotor'
        WHEN (SELECT a.answer_value 
              FROM surveys_answer a
              JOIN surveys_question q ON a.question_id = q.id
              WHERE a.response_id = sr.id 
              AND q.question_type = 'nps'
              LIMIT 1)::INTEGER >= 7 THEN 'Neutro'
        WHEN (SELECT a.answer_value 
              FROM surveys_answer a
              JOIN surveys_question q ON a.question_id = q.id
              WHERE a.response_id = sr.id 
              AND q.question_type = 'nps'
              LIMIT 1)::INTEGER IS NOT NULL THEN 'Detrator'
        ELSE NULL
    END AS classificacao_nps,
    -- Contagem de respostas
    (SELECT COUNT(*) FROM surveys_answer WHERE response_id = sr.id) AS total_perguntas_respondidas,
    -- Total de respostas por pesquisa
    (SELECT COUNT(*) FROM surveys_surveyresponse WHERE survey_id = sr.survey_id) AS total_respostas_pesquisa
FROM surveys_surveyresponse sr
LEFT JOIN surveys_survey s ON sr.survey_id = s.id
LEFT JOIN surveys_surveyinvitation si ON sr.invitation_id = si.id
WHERE sr.respondent_email IS NOT NULL 
AND sr.respondent_email != '';

COMMENT ON VIEW vw_powerbi_respostas IS 'View com dados das respostas recebidas - otimizada para Power BI';
COMMENT ON COLUMN vw_powerbi_respostas.email_respondente IS 'Chave de conexão: Email do respondente';

-- ============================================================================
-- VIEW 2: vw_powerbi_envios
-- Descrição: Tabela com dados de envio de convites
-- Chave: email (email do destinatário)
-- ============================================================================
CREATE OR REPLACE VIEW vw_powerbi_envios AS
SELECT 
    si.id AS envio_id,
    si.email AS email_destinatario,
    si.survey_id AS pesquisa_id,
    s.title AS titulo_pesquisa,
    si.created_at AS data_envio,
    DATE(si.created_at) AS data_envio_date,
    EXTRACT(YEAR FROM si.created_at) AS ano_envio,
    EXTRACT(MONTH FROM si.created_at) AS mes_envio,
    EXTRACT(DAY FROM si.created_at) AS dia_envio,
    TO_CHAR(si.created_at, 'YYYY-MM') AS ano_mes_envio,
    si.unique_token AS token_convite,
    si.is_used AS foi_utilizado,
    si.used_at AS data_utilizacao,
    si.expires_at AS data_expiracao,
    CASE 
        WHEN si.expires_at < CURRENT_TIMESTAMP THEN 'Expirado'
        WHEN si.is_used = TRUE THEN 'Utilizado'
        WHEN si.expires_at >= CURRENT_TIMESTAMP THEN 'Válido'
        ELSE 'Inválido'
    END AS status_convite,
    -- Dias desde o envio
    EXTRACT(DAY FROM (CURRENT_TIMESTAMP - si.created_at)) AS dias_desde_envio,
    -- Dias até expirar (se ainda válido)
    CASE 
        WHEN si.expires_at > CURRENT_TIMESTAMP 
        THEN EXTRACT(DAY FROM (si.expires_at - CURRENT_TIMESTAMP))
        ELSE NULL
    END AS dias_ate_expiracao,
    -- Se foi respondido
    CASE 
        WHEN si.is_used = TRUE THEN 'Sim'
        ELSE 'Não'
    END AS foi_respondido,
    -- Tempo até resposta (se respondido)
    CASE 
        WHEN si.used_at IS NOT NULL 
        THEN EXTRACT(DAY FROM (si.used_at - si.created_at)) * 24 + 
             EXTRACT(HOUR FROM (si.used_at - si.created_at))
        ELSE NULL
    END AS horas_ate_resposta
FROM surveys_surveyinvitation si
LEFT JOIN surveys_survey s ON si.survey_id = s.id;

COMMENT ON VIEW vw_powerbi_envios IS 'View com dados de envio de convites - otimizada para Power BI';
COMMENT ON COLUMN vw_powerbi_envios.email_destinatario IS 'Chave de conexão: Email do destinatário';

-- ============================================================================
-- VIEW 3: vw_powerbi_respondentes
-- Descrição: Cadastro de possíveis respondentes
-- Chave: email (email do usuário)
-- ============================================================================
-- NOTA: Esta view espera uma tabela 'respondents' que precisa ser criada
-- Se não existir, a view retornará dados vazios até a tabela ser criada
-- ============================================================================
CREATE OR REPLACE VIEW vw_powerbi_respondentes AS
SELECT 
    r.id AS respondente_id,
    r.email AS email_usuario,
    r.nome_conta AS nome_conta,
    r.nome_usuario AS nome_usuario,
    r.status_usuario AS status_usuario,
    r.created_at AS data_cadastro,
    DATE(r.created_at) AS data_cadastro_date,
    r.updated_at AS data_atualizacao,
    -- Estatísticas de envios
    (SELECT COUNT(*) 
     FROM surveys_surveyinvitation si 
     WHERE si.email = r.email) AS total_envios_recebidos,
    -- Estatísticas de respostas
    (SELECT COUNT(*) 
     FROM surveys_surveyresponse sr 
     WHERE sr.respondent_email = r.email) AS total_respostas_enviadas,
    -- Taxa de resposta
    CASE 
        WHEN (SELECT COUNT(*) FROM surveys_surveyinvitation WHERE email = r.email) > 0
        THEN ROUND(
            (SELECT COUNT(*)::NUMERIC FROM surveys_surveyresponse WHERE respondent_email = r.email) /
            (SELECT COUNT(*)::NUMERIC FROM surveys_surveyinvitation WHERE email = r.email) * 100,
            2
        )
        ELSE 0
    END AS taxa_resposta_percentual,
    -- Última resposta
    (SELECT MAX(submitted_at) 
     FROM surveys_surveyresponse 
     WHERE respondent_email = r.email) AS ultima_resposta_data,
    -- Último envio
    (SELECT MAX(created_at) 
     FROM surveys_surveyinvitation 
     WHERE email = r.email) AS ultimo_envio_data
FROM respondents r
WHERE r.email IS NOT NULL 
AND r.email != '';

COMMENT ON VIEW vw_powerbi_respondentes IS 'View com cadastro de respondentes - otimizada para Power BI';
COMMENT ON COLUMN vw_powerbi_respondentes.email_usuario IS 'Chave de conexão: Email do usuário';

-- ============================================================================
-- VIEW 4: vw_powerbi_consolidado (BONUS)
-- Descrição: View consolidada com todas as informações relacionadas por email
-- ============================================================================
CREATE OR REPLACE VIEW vw_powerbi_consolidado AS
SELECT 
    emails.email,
    -- Dados do respondente
    r.nome_conta,
    r.nome_usuario,
    r.status_usuario,
    -- Dados de envio
    COALESCE(e.total_envios_recebidos, 0) AS total_envios_recebidos,
    e.ultimo_envio_data,
    -- Dados de resposta
    COALESCE(resp.total_respostas_enviadas, 0) AS total_respostas_enviadas,
    resp.ultima_resposta_data,
    resp.resposta_nps,
    resp.classificacao_nps,
    -- Métricas consolidadas
    CASE 
        WHEN COALESCE(e.total_envios_recebidos, 0) > 0
        THEN ROUND(COALESCE(resp.total_respostas_enviadas, 0)::NUMERIC / e.total_envios_recebidos::NUMERIC * 100, 2)
        ELSE 0
    END AS taxa_resposta_percentual
FROM (
    SELECT DISTINCT email_usuario AS email FROM vw_powerbi_respondentes
    UNION
    SELECT DISTINCT email_destinatario AS email FROM vw_powerbi_envios
    UNION
    SELECT DISTINCT email_respondente AS email FROM vw_powerbi_respostas
) emails
LEFT JOIN (
    SELECT 
        email_usuario AS email,
        MAX(nome_conta) AS nome_conta,
        MAX(nome_usuario) AS nome_usuario,
        MAX(status_usuario) AS status_usuario
    FROM vw_powerbi_respondentes
    GROUP BY email_usuario
) r ON emails.email = r.email
LEFT JOIN (
    SELECT 
        email_destinatario AS email,
        COUNT(*) AS total_envios_recebidos,
        MAX(data_envio) AS ultimo_envio_data
    FROM vw_powerbi_envios
    GROUP BY email_destinatario
) e ON emails.email = e.email
LEFT JOIN (
    SELECT 
        email_respondente AS email,
        COUNT(*) AS total_respostas_enviadas,
        MAX(data_resposta) AS ultima_resposta_data,
        MAX(resposta_nps) AS resposta_nps,
        MAX(classificacao_nps) AS classificacao_nps
    FROM vw_powerbi_respostas
    GROUP BY email_respondente
) resp ON emails.email = resp.email
WHERE emails.email IS NOT NULL;

COMMENT ON VIEW vw_powerbi_consolidado IS 'View consolidada com todas as informações por email - otimizada para Power BI';

-- ============================================================================
-- ÍNDICES PARA OTIMIZAÇÃO (já devem existir, mas garantindo)
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_surveyresponse_email ON surveys_surveyresponse(respondent_email);
CREATE INDEX IF NOT EXISTS idx_surveyinvitation_email ON surveys_surveyinvitation(email);
CREATE INDEX IF NOT EXISTS idx_surveyresponse_submitted_at ON surveys_surveyresponse(submitted_at);
CREATE INDEX IF NOT EXISTS idx_surveyinvitation_created_at ON surveys_surveyinvitation(created_at);

-- ============================================================================
-- VERIFICAÇÃO FINAL
-- ============================================================================
DO $$
BEGIN
    RAISE NOTICE 'Views criadas com sucesso!';
    RAISE NOTICE 'Views disponiveis:';
    RAISE NOTICE '  - vw_powerbi_respostas';
    RAISE NOTICE '  - vw_powerbi_envios';
    RAISE NOTICE '  - vw_powerbi_respondentes (requer tabela respondents)';
    RAISE NOTICE '  - vw_powerbi_consolidado';
END $$;

-- ============================================================================
-- FIM DO SCRIPT
-- ============================================================================
