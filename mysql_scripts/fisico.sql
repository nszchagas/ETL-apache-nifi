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
CREATE TABLE IF NOT EXISTS INVESTIGACAO (
    idInvestigacao BIGINT PRIMARY KEY AUTO_INCREMENT,
    DTINVESTIG DATE,
    FONTEINV ENUM ('1', '2', '3', '4', '5', '6', '7', '8', '9'),
    DTCADINV DATE,
    DTCONINV DATE,
    TPNIVELINV ENUM ('E', 'R', 'M'),
    TPRESGINFO ENUM ('1', '2', '3')
) ENGINE = InnoDB AUTO_INCREMENT = 1;

-- --8 < -- [end:mortalidade]
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

CREATE TABLE IF NOT EXISTS PESSOA_FALECIDA (
    idPessoaFalecida BIGINT PRIMARY KEY,
    `NATURAL` INT,
    CODMUNRES INT,
    CODMUNNATU INT,
    DTNASC DATETIME,
    IDADE VARCHAR(10),
    SEXO VARCHAR(10),
    RACACOR VARCHAR(10),
    ESTCIV ENUM ('1', '2', '3', '4', '5', '9'),
    ESC ENUM ('1', '2', '3', '4', '5', '9'),
    ESC2010 ENUM ('1', '2', '3', '4', '5', '9'),
    SERIESCFAL ENUM ('1', '2', '3', '4', '5', '6', '7', '8'),
    OCUP INT,
    IDADEMAE INT,
    ESCMAE ENUM ('1', '2', '3', '4', '5', '9'),
    ESCMAE2010 ENUM ('1', '2', '3', '4', '5', '9'),
    SERIESCMAE INT,
    OCUPMAE INT,
    QTDFILVIVO INT,
    QTDFILMORT INT,
    GRAVIDEZ ENUM ('1', '2', '3', '9'),
    SEMAGESTAC INT,
    GESTACAO ENUM ('1', '2', '3', '4', '5', '6'),
    PARTO ENUM ('1', '2', '9'),
    PESO INT,
    ESCMAEAGR1 ENUM (
        '00',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '10',
        '11',
        '12'
    ),
    ESCFALAGR1 ENUM (
        '00',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '10',
        '11',
        '12'
    ),
    NUMEROLOTE BIGINT
);