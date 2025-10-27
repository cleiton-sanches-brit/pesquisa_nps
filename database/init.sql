-- Script de inicialização do banco de dados NPS Surveys
-- Execute este script no SQL Server Management Studio ou via sqlcmd

-- Criar banco de dados
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'survey_analytics')
BEGIN
    CREATE DATABASE survey_analytics;
END
GO

USE survey_analytics;
GO

-- Configurar collation para suporte a caracteres especiais
ALTER DATABASE survey_analytics COLLATE SQL_Latin1_General_CP1_CI_AS;
GO

-- Criar usuário para a aplicação (opcional)
-- Descomente e configure conforme necessário
/*
IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = 'nps_user')
BEGIN
    CREATE LOGIN nps_user WITH PASSWORD = 'YourStrong@Passw0rd';
END
GO

IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'nps_user')
BEGIN
    CREATE USER nps_user FOR LOGIN nps_user;
    ALTER ROLE db_datareader ADD MEMBER nps_user;
    ALTER ROLE db_datawriter ADD MEMBER nps_user;
    ALTER ROLE db_ddladmin ADD MEMBER nps_user;
END
GO
*/

PRINT 'Banco de dados survey_analytics configurado com sucesso!';
