CREATE DATABASE IF NOT EXISTS sim_datasus;

USE sim_datasus;

-- --8 < -- [start:cid]
CREATE TABLE IF NOT EXISTS cid_10 (
    codigo VARCHAR(10) NOT NULL PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL
);

-- --8<-- [end:cid]
-- --8<-- [start:metadados]
USE sim_datasus;

CREATE TABLE IF NOT EXISTS metadados_sistema (
    idMetadados BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    -- Campo CONTADOR ou CONTADOR.1 nos dados originais
    idObito VARCHAR(8) NOT NULL UNIQUE,
    -- Campo ORIGEM nos dados originais
    origemDados ENUM (
        'ORACLE',
        'BANCO ESTADUAL',
        'BANCO SEADE',
        'IGNORADO'
    ) NOT NULL DEFAULT 'IGNORADO',
    -- Campo CODIFICADO nos dados originais
    formCodificado BOOLEAN NOT NULL DEFAULT FALSE,
    -- Campo VERSAOSIST nos dados originais
    versaoSistema VARCHAR(10)
) ENGINE = InnoDB AUTO_INCREMENT = 1;

-- --8<-- [end:metadados]
-- --8<-- [start:investigacao]
CREATE TABLE IF NOT EXISTS investigacao (
    idInvestigacao BIGINT PRIMARY KEY AUTO_INCREMENT,
    idOBito VARCHAR(8) NOT NULL UNIQUE,
    fonteInvestigacao ENUM( 'ComiteDeMorteMaternaOuInfantil' , 'VisitaDomiciliar' , 'Prontuario' , 'RelacionadoComOutrosBancosDeDados' , 'SVO' , 'IML' , 'OutraFonte' , 'MultiplasFontes' , 'Ignorado'),
    dtInicio DATE,
    dtcadastro   DATE,
    dtConclusao   DATE,
    nivelInvestigador ENUM('ESTADUAL', 'REGIONAL', 'MUNICIPAL'),
    tipoResgateInformacao ENUM( 'NAO_ACRESCENTOU','SIM_NOVAS_INFORMACOES','SIM_CORRECAO_CAUSAS')
) ENGINE = InnoDB AUTO_INCREMENT = 1;
-- --8 < -- [end:investigacao]

-- --8 <-- [start: pessoa_falecida]
CREATE TABLE IF NOT EXISTS pessoa_falecida (
    idPessoaFalecida BIGINT PRIMARY KEY AUTO_INCREMENT,
    naturalidade INT,
    codMunResidencia INT,
    codMunNaturalidade INT,
    dtNascimento DATETIME,
    sexo VARCHAR(10),
    etnia ENUM ('BRANCA','PRETA','AMARELA','PARDA','INDIGENA'),
    estadoCivil ENUM ('SOLTEIRO', 'CASADO','VIUVO','SEPARADO','UNIAO_CONSENSUAL','IGNORADO'),
    escolaridade ENUM ('NENHUMA', 'DE_1_A_3_ANOS', 'DE_4_A_7_ANOS', 'DE_8_A_11_ANOS', '12_ANOS_E_MAIS', 'IGNORADO'),
    codOcupacao INT,
    qtdFilhosVivos INT NOT NULL DEFAULT 0,
    qtdFilhosMortos INT NOT NULL DEFAULT 0,
    tipoGravidez ENUM ('1', '2', '3', '9'),
    semanasGestacao INT,
    tipoParto ENUM ('1', '2', '9'),
    pesoEmGramas INT,
    numeroLote BIGINT
) ENGINE InnoDB AUTO_INCREMENT = 1;
-- --8 < -- [end: pessoa_falecida]

CREATE TABLE IF NOT EXISTS OBITO (
    idObito BIGINT PRIMARY KEY,
    TIPOBITO ENUM ('1', '2'),
    DTOBITO DATE,
    HORAOBITO TIMESTAMP,
    OBITOPARTO ENUM ('1', '2', '3', '9'),
    OBITOGRAV BOOLEAN,
    OBITOPUERP ENUM ('1', '2', '3', '9'),
    CIRCOBITO ENUM ('1', '2', '3', '4', '9'),
    TPOBITOCOR ENUM ('1', '2', '3', '4', '5', '6', '7', '8', '9'),
    LOCOCOR ENUM ('1', '2', '3', '4', '5', '6', '9'),
    CODESTAB INT,
    CODMUNOCOR INT,
    TPMORTEOCO ENUM ('1', '2', '3', '4', '5', '8', '9'),
    ASSISTMED BOOLEAN,
    EXAME BOOLEAN,
    CIRURGIA BOOLEAN,
    NECROPSIA BOOLEAN,
    LINHAA VARCHAR(20),
    LINHAB VARCHAR(20),
    LINHAC VARCHAR(20),
    LINHAD VARCHAR(20),
    LINHAII VARCHAR(40),
    CAUSABAS VARCHAR(10),
    CB_PRE VARCHAR(10),
    COMUNSVOIM INT,
    DTATESTADO DATETIME,
    ACIDTRAB BOOLEAN NOT NULL,
    FONTE ENUM ('1', '2', '3', '4', '9'),
    ALTCAUSA BOOLEAN,
    DTCADASTRO DATETIME,
    ATESTANTE VARCHAR(10),
    DTRECEBIM DATETIME,
    ATESTADO VARCHAR(100),
    DTRECORIGA DATETIME,
    CAUSAMAT VARCHAR(10),
    STDOEPIDEM BOOLEAN NOT NULL,
    STDONOVA BOOLEAN NOT NULL,
    DIFDATA INT,
    NUDIASOBCO INT,
    FONTES VARCHAR(6),
    DTCADINF DATETIME,
    DTCONCASO DATETIME,
    CAUSABAS_O VARCHAR(10),
    TPPOS BOOLEAN NOT NULL,
    TP_ALTERA INT,
    CB_ALT VARCHAR(10)
);
