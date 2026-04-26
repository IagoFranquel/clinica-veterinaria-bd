-- ============================================================
--  CLÍNICA VETERINÁRIA PATINHA FELIZ — DQL
--  Consultas: filtros, ordenação, INNER JOIN, LEFT JOIN
-- ============================================================

-- ------------------------------------------------------------
-- 1. INNER JOIN — Consultas com dados do animal e veterinário
-- ------------------------------------------------------------
SELECT
    c.id                            AS consulta_id,
    TO_CHAR(c.data_consulta, 'DD/MM/YYYY HH24:MI') AS data_hora,
    a.nome                          AS animal,
    a.especie,
    t.nome                          AS tutor,
    v.nome                          AS veterinario,
    v.especialidade,
    c.motivo,
    c.diagnostico,
    c.valor
FROM consultas c
INNER JOIN animais      a ON c.animal_id      = a.id
INNER JOIN tutores      t ON a.tutor_id       = t.id
INNER JOIN veterinarios v ON c.veterinario_id = v.id
ORDER BY c.data_consulta DESC;

-- ------------------------------------------------------------
-- 2. LEFT JOIN — Todos os animais, mesmo sem consultas
-- ------------------------------------------------------------
SELECT
    a.nome          AS animal,
    a.especie,
    a.raca,
    t.nome          AS tutor,
    COUNT(c.id)     AS total_consultas,
    MAX(c.data_consulta) AS ultima_consulta
FROM animais a
LEFT JOIN tutores   t ON a.tutor_id = t.id
LEFT JOIN consultas c ON c.animal_id = a.id
GROUP BY a.id, a.nome, a.especie, a.raca, t.nome
ORDER BY total_consultas DESC;

-- ------------------------------------------------------------
-- 3. Filtro — Consultas de um tutor específico (por nome)
-- ------------------------------------------------------------
SELECT
    c.id,
    TO_CHAR(c.data_consulta, 'DD/MM/YYYY') AS data,
    a.nome  AS animal,
    v.nome  AS veterinario,
    c.motivo,
    c.valor
FROM consultas c
INNER JOIN animais      a ON c.animal_id      = a.id
INNER JOIN tutores      t ON a.tutor_id       = t.id
INNER JOIN veterinarios v ON c.veterinario_id = v.id
WHERE LOWER(t.nome) LIKE LOWER('%Ana%')
ORDER BY c.data_consulta DESC;

-- ------------------------------------------------------------
-- 4. Ordenação — Animais ordenados por peso DESC
-- ------------------------------------------------------------
SELECT
    a.nome,
    a.especie,
    a.raca,
    a.peso_kg,
    t.nome AS tutor
FROM animais a
INNER JOIN tutores t ON a.tutor_id = t.id
ORDER BY a.peso_kg DESC;

-- ------------------------------------------------------------
-- 5. Faturamento por veterinário (INNER JOIN + GROUP BY)
-- ------------------------------------------------------------
SELECT
    v.nome          AS veterinario,
    v.especialidade,
    COUNT(c.id)     AS total_consultas,
    SUM(c.valor)    AS faturamento_total,
    AVG(c.valor)    AS ticket_medio
FROM veterinarios v
INNER JOIN consultas c ON c.veterinario_id = v.id
GROUP BY v.id, v.nome, v.especialidade
ORDER BY faturamento_total DESC;

-- ------------------------------------------------------------
-- 6. Consultas em intervalo de datas
-- ------------------------------------------------------------
SELECT
    TO_CHAR(c.data_consulta, 'DD/MM/YYYY') AS data,
    a.nome  AS animal,
    t.nome  AS tutor,
    v.nome  AS veterinario,
    c.motivo,
    c.valor
FROM consultas c
INNER JOIN animais      a ON c.animal_id      = a.id
INNER JOIN tutores      t ON a.tutor_id       = t.id
INNER JOIN veterinarios v ON c.veterinario_id = v.id
WHERE c.data_consulta BETWEEN '2025-01-01' AND '2025-12-31'
ORDER BY c.data_consulta;
