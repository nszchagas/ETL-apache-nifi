CREATE DATABASE IF NOT EXISTS sim_datasus;

USE sim_datasus;

-- --8<-- [start:cid]
CREATE TABLE CID10
(
    codigo    VARCHAR(10)  NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    CONSTRAINT cid10_pk PRIMARY KEY (codigo)
) ENGINE = InnoDB;

-- --8<-- [end:cid]
-- --8<-- [start:metadados]

CREATE TABLE METADADOS_SISTEMA
(

    idMetadados    BIGINT  NOT NULL AUTO_INCREMENT,
    idObito        BIGINT  NOT NULL,
    -- Campo ORIGEM nos dados originais
    origemDados    ENUM ('ORACLE',
        'BANCO_ESTADUAL',
        'BANCO_SEADE',
        'IGNORADO' )       NOT NULL DEFAULT 'IGNORADO',
    -- Campo CODIFICADO nos dados originais
    formCodificado BOOLEAN NOT NULL DEFAULT FALSE,
    -- Campo VERSAOSIST nos dados originais
    versaoSistema  VARCHAR(10),
    CONSTRAINT metadados_sistema_pk PRIMARY KEY (idMetadados),
    CONSTRAINT metadados_sistema__obito_fk FOREIGN KEY (idObito) REFERENCES OBITO (idObito),
    CONSTRAINT metadados_sistema__obito_uk UNIQUE (idObito)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1;

-- --8<-- [end:metadados]
-- --8<-- [start:investigacao]
CREATE TABLE INVESTIGACAO
(
    idInvestigacao        BIGINT NOT NULL AUTO_INCREMENT,
    idOBito               BIGINT NOT NULL,
    fonteInvestigacao     ENUM ('CMMI',
        'ENTREVISTA_FAMILIA',
        'PRONTUARIO',
        'BANCOS_DE_DADOS',
        'SVO',
        'IML',
        'OUTRA',
        'MULTIPLAS_FONTES',
        'IGNORADO')              NOT NULL DEFAULT 'IGNORADO',
    tipoResgateInformacao ENUM ('NAO_ACRESCENTOU',
        'SIM_NOVAS_INFOS',
        'SIM_CORRECAO')          NOT NULL DEFAULT 'NAO_ACRESCENTOU',
    dtInicio              DATE,
    dtcadastro            DATE,
    dtConclusao           DATE,
    nivelInvestigador     ENUM ('ESTADUAL',
        'REGIONAL',
        'MUNICIPAL'),
    CONSTRAINT investigacao_pk PRIMARY KEY (idInvestigacao),
    CONSTRAINT investigacao__obito_fk FOREIGN KEY (idObito) REFERENCES OBITO (idObito),
    CONSTRAINT investigacao_sistema__obito_uk UNIQUE (idObito)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1;
-- --8<-- [end:investigacao]

-- --8<-- [start: pessoa_falecida]
CREATE TABLE PESSOA_FALECIDA
(
    idPessoaFalecida   BIGINT PRIMARY KEY AUTO_INCREMENT,
    idObito            BIGINT NOT NULL,
    naturalidade       INT,
    codMunResidencia   INT,
    codMunNaturalidade INT,
    dtNascimento       DATE,
    sexo               ENUM ('M',
        'F',
        'IGNORADO')           NOT NULL DEFAULT 'IGNORADO',
    etnia              ENUM ('BRANCA',
        'PRETA',
        'AMARELA',
        'PARDA',
        'INDIGENA'),
    estadoCivil        ENUM ('SOLTEIRO',
        'CASADO',
        'VIUVO',
        'SEPARADO',
        'UNIAO_CONSENSUAL',
        'IGNORADO')           NOT NULL DEFAULT 'IGNORADO',
    escolaridade       ENUM ('NENHUMA',
        'DE_1_A_3_ANOS',
        'DE_4_A_7_ANOS',
        'DE_8_A_11_ANOS',
        '12_ANOS_E_MAIS',
        'IGNORADO' )          NOT NULL DEFAULT 'IGNORADO',
    CONSTRAINT pessoa_falecida_pk PRIMARY KEY (idPessoaFalecida),
    CONSTRAINT pessoa_falecida__obito_fk FOREIGN KEY (idObito) REFERENCES OBITO (idObito),
    CONSTRAINT pessoa_falecida_sistema__obito_uk UNIQUE (idObito)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1;
-- --8<-- [end: pessoa_falecida]
-- --8<-- [start: obito]
CREATE TABLE OBITO
(
    -- Campo CONTADOR ou CONTADOR.1 nos dados originais
    idObito               BIGINT      NOT NULL,
    idDiagnostico         BIGINT      NOT NULL,
    causaBasica           VARCHAR(10) NOT NULL,
    dataHora              TIMESTAMP   NOT NULL,
    circunstancia         ENUM ('ACIDENTE',
        'SUICIDIO',
        'HOMICIO',
        'OUTROS',
        'IGNORADO')                   NOT NULL DEFAULT 'IGNORADO',
    isObitoFetal          BOOLEAN     NOT NULL DEFAULT FALSE,
    houveAlteracaoCausa   BOOLEAN     NOT NULL DEFAULT FALSE,
    obitoEmRelacaoAoParto ENUM ('ANTES',
        'DURANTE',
        'DEPOIS',
        'IGNORADO' )                  NOT NULL DEFAULT 'IGNORADO',
    crmAtestante          VARCHAR(10) NOT NULL,
    CONSTRAINT obito_pf PRIMARY KEY (idObito),
    CONSTRAINT obito_cid10_fk FOREIGN KEY (causaBasica) REFERENCES CID10 (codigo),
    CONSTRAINT obito_diagnostico_fk FOREIGN KEY (idDiagnostico) REFERENCES DIAGNOSTICO (idDiagnostico)

) ENGINE = InnoDB;

CREATE TABLE causa_secundaria_morte
(
    idObito BIGINT      NOT NULL,
    codCid  VARCHAR(10) NOT NULL,
    CONSTRAINT obito_cid_uk UNIQUE (idObito, codCid),
    CONSTRAINT obito_cid_obito_fk FOREIGN KEY (idObito) REFERENCES OBITO (idObito),
    CONSTRAINT obito_cid_cid_fk FOREIGN KEY (codCid) REFERENCES CID10 (codigo)

) ENGINE = InnoDB;

CREATE TABLE DIAGNOSTICO
(
    idDiagnostico      BIGINT AUTO_INCREMENT,
    diagnosticoLinhaA  VARCHAR(20) NOT NULL,
    diagnosticoLinhaB  VARCHAR(20),
    diagnosticoLinhaC  VARCHAR(20),
    diagnosticoLinhaD  VARCHAR(20),
    diagnosticoLinhaII VARCHAR(40),
    CONSTRAINT diagnostico_pk PRIMARY KEY (idDiagnostico)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1;
-- --8<-- [end: obito]

