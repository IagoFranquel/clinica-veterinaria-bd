-- ============================================================
--  CLÍNICA VETERINÁRIA PATINHA FELIZ — DML
--  Exemplos de INSERT, UPDATE e DELETE
-- ============================================================

-- ------------------------------------------------------------
-- INSERTS — Tutores
-- ------------------------------------------------------------
INSERT INTO tutores (nome, cpf, telefone, email, endereco) VALUES
  ('Ana Paula Ferreira',   '01234567890', '(98) 99101-2233', 'ana.paula@email.com',  'Rua das Flores, 10 — São Luís/MA'),
  ('Carlos Henrique Lima', '09876543211', '(98) 98765-4321', 'carloslima@email.com', 'Av. Getúlio Vargas, 55 — Imperatriz/MA'),
  ('Fernanda Sousa',       '05566778899', '(98) 91234-5678', 'fernanda@email.com',   'Rua Tiradentes, 200 — Caxias/MA'),
  ('Roberto Alves',        '01122334455', '(98) 98888-0011', 'roberto@email.com',    'Rua da Paz, 77 — Timon/MA');

-- ------------------------------------------------------------
-- INSERTS — Veterinários
-- ------------------------------------------------------------
INSERT INTO veterinarios (nome, crmv, especialidade, telefone) VALUES
  ('Dra. Márcia Teles',    'MA-00123', 'Clínica Geral',      '(98) 99000-1111'),
  ('Dr. Lucas Fonseca',    'MA-00456', 'Ortopedia',          '(98) 99000-2222'),
  ('Dra. Juliana Ramos',   'MA-00789', 'Dermatologia',       '(98) 99000-3333'),
  ('Dr. Antônio Cardoso',  'MA-01011', 'Cardiologia',        '(98) 99000-4444');

-- ------------------------------------------------------------
-- INSERTS — Animais
-- ------------------------------------------------------------
INSERT INTO animais (nome, especie, raca, data_nasc, peso_kg, tutor_id) VALUES
  ('Mel',     'Cão',  'Golden Retriever',  '2020-03-15', 28.5, 1),
  ('Bolinha',  'Cão',  'Poodle',            '2021-07-22', 5.2,  1),
  ('Mimi',    'Gato', 'Siamês',            '2019-11-01', 4.1,  2),
  ('Leão',    'Cão',  'Pastor Alemão',     '2018-06-10', 35.0, 3),
  ('Nina',    'Gato', 'Persa',             '2022-01-30', 3.8,  4),
  ('Tobias',  'Cão',  'Labrador',          '2020-09-05', 30.2, 4);

-- ------------------------------------------------------------
-- INSERTS — Consultas
-- ------------------------------------------------------------
INSERT INTO consultas (animal_id, veterinario_id, data_consulta, motivo, diagnostico, prescricao, valor) VALUES
  (1, 1, '2025-01-10 09:00', 'Check-up anual',            'Animal saudável',             'Vermífugo semestral',           150.00),
  (2, 3, '2025-01-15 10:30', 'Coceira excessiva',         'Dermatite alérgica',          'Shampoo hipoalergênico + apoquel', 200.00),
  (3, 1, '2025-02-03 14:00', 'Perda de apetite',          'Estresse pós-mudança',        'Calmante natural 15 dias',       180.00),
  (4, 2, '2025-02-20 08:30', 'Claudicação membro traseiro','Displasia leve',              'Fisioterapia + condroitina',     350.00),
  (5, 1, '2025-03-05 11:00', 'Check-up anual',            'Animal saudável',             'Vacinação em dia',              130.00),
  (6, 4, '2025-03-18 09:45', 'Cansaço excessivo',         'Sopro cardíaco grau II',      'Enalapril 2,5mg/dia',           420.00),
  (1, 1, '2025-04-01 10:00', 'Retorno — vermífugo',       'Evolução positiva',           'Alta',                          80.00);

-- ------------------------------------------------------------
-- UPDATE — Atualizar peso de um animal
-- ------------------------------------------------------------
UPDATE animais SET peso_kg = 29.0 WHERE id = 1;

-- UPDATE — Marcar veterinário como inativo
UPDATE veterinarios SET ativo = FALSE WHERE id = 4;

-- UPDATE — Corrigir diagnóstico de uma consulta
UPDATE consultas SET diagnostico = 'Dermatite alérgica leve' WHERE id = 2;

-- ------------------------------------------------------------
-- DELETE — Remover consulta específica (exemplo)
-- ------------------------------------------------------------
-- DELETE FROM consultas WHERE id = 7;

-- DELETE — Remover tutor (cascata remove animais e consultas)
-- DELETE FROM tutores WHERE id = 4;
