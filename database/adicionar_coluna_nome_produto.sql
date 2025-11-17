-- Script SQL para adicionar coluna nome_produto na tabela surveys_respondent
-- Execute este script no Supabase SQL Editor

-- Adicionar coluna nome_produto
ALTER TABLE surveys_respondent 
ADD COLUMN IF NOT EXISTS nome_produto VARCHAR(200) NULL;

-- Adicionar comentário na coluna (opcional)
COMMENT ON COLUMN surveys_respondent.nome_produto IS 'Nome do produto vinculado ao respondente';

-- Verificar se a coluna foi criada
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'surveys_respondent' 
AND column_name = 'nome_produto';

