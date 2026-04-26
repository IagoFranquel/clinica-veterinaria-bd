-- ============================================================
--  CLÍNICA VETERINÁRIA PATINHA FELIZ — DDL
--  Banco de Dados: PostgreSQL
-- ============================================================

-- Remove tabelas se já existirem (ordem inversa das FKs)
DROP TABLE IF EXISTS consultas CASCADE;
DROP TABLE IF EXISTS animais   CASCADE;
DROP TABLE IF EXISTS tutores   CASCADE;
DROP TABLE IF EXISTS veterinarios CASCADE;

-- ------------------------------------------------------------
-- 1. TUTORES
-- ------------------------------------------------------------
CREATE TABLE tutores (
    id          SERIAL       PRIMARY KEY,
    nome        VARCHAR(120) NOT NULL,
    cpf         CHAR(11)     NOT NULL UNIQUE,
    telefone    VARCHAR(20),
    email       VARCHAR(100),
    endereco    TEXT,
    criado_em   TIMESTAMP    DEFAULT NOW()
);

-- ------------------------------------------------------------
-- 2. VETERINÁRIOS
-- ------------------------------------------------------------
CREATE TABLE veterinarios (
    id          SERIAL       PRIMARY KEY,
    nome        VARCHAR(120) NOT NULL,
    crmv        VARCHAR(20)  NOT NULL UNIQUE,
    especialidade VARCHAR(80),
    telefone    VARCHAR(20),
    ativo       BOOLEAN      DEFAULT TRUE,
    criado_em   TIMESTAMP    DEFAULT NOW()
);

-- ------------------------------------------------------------
-- 3. ANIMAIS
-- ------------------------------------------------------------
CREATE TABLE animais (
    id          SERIAL       PRIMARY KEY,
    nome        VARCHAR(80)  NOT NULL,
    especie     VARCHAR(50)  NOT NULL,
    raca        VARCHAR(80),
    data_nasc   DATE,
    peso_kg     NUMERIC(5,2),
    tutor_id    INTEGER      NOT NULL REFERENCES tutores(id) ON DELETE CASCADE,
    criado_em   TIMESTAMP    DEFAULT NOW()
);

-- ------------------------------------------------------------
-- 4. CONSULTAS
-- ------------------------------------------------------------
CREATE TABLE consultas (
    id              SERIAL       PRIMARY KEY,
    animal_id       INTEGER      NOT NULL REFERENCES animais(id)     ON DELETE CASCADE,
    veterinario_id  INTEGER      NOT NULL REFERENCES veterinarios(id) ON DELETE RESTRICT,
    data_consulta   TIMESTAMP    NOT NULL DEFAULT NOW(),
    motivo          TEXT         NOT NULL,
    diagnostico     TEXT,
    prescricao      TEXT,
    valor           NUMERIC(8,2) NOT NULL DEFAULT 0.00,
    criado_em       TIMESTAMP    DEFAULT NOW()
);

-- ------------------------------------------------------------
-- Índices úteis
-- ------------------------------------------------------------
CREATE INDEX idx_animais_tutor    ON animais(tutor_id);
CREATE INDEX idx_consultas_animal ON consultas(animal_id);
CREATE INDEX idx_consultas_vet    ON consultas(veterinario_id);
CREATE INDEX idx_consultas_data   ON consultas(data_consulta);
