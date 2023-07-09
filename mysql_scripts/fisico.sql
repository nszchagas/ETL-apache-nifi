CREATE DATABASE IF NOT EXISTS sim_datasus;

USE sim_datasus;

CREATE TABLE CID10
(
    codigo    VARCHAR(10)  NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    CONSTRAINT cid10_pk PRIMARY KEY (codigo)
) ENGINE = InnoDB;


CREATE TABLE OBITO
(
    -- Campo CONTADOR ou CONTADOR.1 nos dados originais
    idObito               BIGINT      NOT NULL,
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
    crmAtestante          VARCHAR(10),
    CONSTRAINT obito_pf PRIMARY KEY (idObito),
    CONSTRAINT obito_cid10_fk FOREIGN KEY (causaBasica) REFERENCES CID10 (codigo)

) ENGINE = InnoDB;



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
    dtCadastro            DATE,
    dtConclusao           DATE,
    nivelInvestigador     ENUM ('ESTADUAL',
        'REGIONAL',
        'MUNICIPAL'),
    CONSTRAINT investigacao_pk PRIMARY KEY (idInvestigacao),
    CONSTRAINT investigacao__obito_fk FOREIGN KEY (idObito) REFERENCES OBITO (idObito),
    CONSTRAINT investigacao_sistema__obito_uk UNIQUE (idObito)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1;



CREATE TABLE PESSOA_FALECIDA
(
    idPessoaFalecida   BIGINT AUTO_INCREMENT,
    idObito            BIGINT NOT NULL,
    dtNascimento       DATE   NOT NULL,
    dtFalecimento      DATE   NOT NULL,
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
    escolaridade       ENUM (
        'NENHUMA',
        'FUND_I_INC',
        'FUND_I_COMP',
        'FUND_II_INC',
        'FUND_II_COMP',
        'MEDIO_INC',
        'MEDIO_COMP',
        'SUPERIOR_INC',
        'SUPERIOR_COMP',
        'IGNORADO')       NOT NULL DEFAULT 'IGNORADO',
    naturalidade       INT,
    codMunResidencia   INT,
    codMunNaturalidade INT,
    CONSTRAINT pessoa_falecida_pk PRIMARY KEY (idPessoaFalecida),
    CONSTRAINT pessoa_falecida__obito_fk FOREIGN KEY (idObito) REFERENCES OBITO (idObito),
    CONSTRAINT pessoa_falecida_sistema__obito_uk UNIQUE (idObito)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1;


CREATE TABLE tem_causas_secundarias_por
(
    idObito BIGINT      NOT NULL,
    codCid  VARCHAR(10) NOT NULL,
    CONSTRAINT obito_cid_uk UNIQUE (idObito, codCid),
    CONSTRAINT obito_cid_obito_fk FOREIGN KEY (idObito) REFERENCES OBITO (idObito),
    CONSTRAINT obito_cid_cid_fk FOREIGN KEY (codCid) REFERENCES CID10 (codigo)

) ENGINE = InnoDB;

CREATE TABLE DIAGNOSTICO
(
    idDiagnostico BIGINT AUTO_INCREMENT,
    idObito       BIGINT      NOT NULL,
    linhaA        VARCHAR(20) NOT NULL,
    linhaB        VARCHAR(20),
    linhaC        VARCHAR(20),
    linhaD        VARCHAR(20),
    linhaII       VARCHAR(40),
    CONSTRAINT diagnostico_pk PRIMARY KEY (idDiagnostico),
    CONSTRAINT diagnostico_obito_fk FOREIGN KEY (idOBito) REFERENCES OBITO (idOBito)

) ENGINE = InnoDB
  AUTO_INCREMENT = 1;


