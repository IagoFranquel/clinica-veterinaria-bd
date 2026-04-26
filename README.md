<svg width="680" height="520" viewBox="0 0 680 520" xmlns="http://www.w3.org/2000/svg">
  <title>DER — Clínica Veterinária Patinha Feliz</title>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="#888" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>

  <!-- TUTORES -->
  <rect x="30" y="30" width="175" height="220" rx="8" fill="#E1F5EE" stroke="#0F6E56" stroke-width="1"/>
  <rect x="30" y="30" width="175" height="36" rx="8" fill="#1D9E75"/>
  <rect x="30" y="52" width="175" height="14" fill="#1D9E75"/>
  <text x="117" y="54" text-anchor="middle" dominant-baseline="central" fill="white" font-size="14" font-weight="bold" font-family="sans-serif">tutores</text>
  <line x1="30" y1="66" x2="205" y2="66" stroke="#0F6E56" stroke-width="0.5"/>
  <text x="44" y="84"  dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#085041">🔑 id (PK)</text>
  <text x="44" y="104" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#085041">nome</text>
  <text x="44" y="124" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#085041">cpf (UNIQUE)</text>
  <text x="44" y="144" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#085041">telefone</text>
  <text x="44" y="164" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#085041">email</text>
  <text x="44" y="184" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#085041">endereco</text>
  <text x="44" y="204" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#085041">criado_em</text>

  <!-- ANIMAIS -->
  <rect x="255" y="30" width="175" height="260" rx="8" fill="#EEEDFE" stroke="#534AB7" stroke-width="1"/>
  <rect x="255" y="30" width="175" height="36" rx="8" fill="#7F77DD"/>
  <rect x="255" y="52" width="175" height="14" fill="#7F77DD"/>
  <text x="342" y="54" text-anchor="middle" dominant-baseline="central" fill="white" font-size="14" font-weight="bold" font-family="sans-serif">animais</text>
  <line x1="255" y1="66" x2="430" y2="66" stroke="#534AB7" stroke-width="0.5"/>
  <text x="269" y="84"  dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#26215C">🔑 id (PK)</text>
  <text x="269" y="104" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#26215C">nome</text>
  <text x="269" y="124" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#26215C">especie</text>
  <text x="269" y="144" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#26215C">raca</text>
  <text x="269" y="164" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#26215C">data_nasc</text>
  <text x="269" y="184" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#26215C">peso_kg</text>
  <text x="269" y="204" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#BA7517">🔗 tutor_id (FK)</text>
  <text x="269" y="224" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#26215C">criado_em</text>

  <!-- VETERINARIOS -->
  <rect x="475" y="30" width="175" height="240" rx="8" fill="#FAECE7" stroke="#993C1D" stroke-width="1"/>
  <rect x="475" y="30" width="175" height="36" rx="8" fill="#D85A30"/>
  <rect x="475" y="52" width="175" height="14" fill="#D85A30"/>
  <text x="562" y="54" text-anchor="middle" dominant-baseline="central" fill="white" font-size="14" font-weight="bold" font-family="sans-serif">veterinarios</text>
  <line x1="475" y1="66" x2="650" y2="66" stroke="#993C1D" stroke-width="0.5"/>
  <text x="489" y="84"  dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#4A1B0C">🔑 id (PK)</text>
  <text x="489" y="104" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#4A1B0C">nome</text>
  <text x="489" y="124" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#4A1B0C">crmv (UNIQUE)</text>
  <text x="489" y="144" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#4A1B0C">especialidade</text>
  <text x="489" y="164" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#4A1B0C">telefone</text>
  <text x="489" y="184" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#4A1B0C">ativo</text>
  <text x="489" y="204" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#4A1B0C">criado_em</text>

  <!-- CONSULTAS -->
  <rect x="255" y="360" width="175" height="140" rx="8" fill="#FAEEDA" stroke="#854F0B" stroke-width="1"/>
  <rect x="255" y="360" width="175" height="36" rx="8" fill="#EF9F27"/>
  <rect x="255" y="382" width="175" height="14" fill="#EF9F27"/>
  <text x="342" y="384" text-anchor="middle" dominant-baseline="central" fill="white" font-size="14" font-weight="bold" font-family="sans-serif">consultas</text>
  <line x1="255" y1="396" x2="430" y2="396" stroke="#854F0B" stroke-width="0.5"/>
  <text x="269" y="412" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#412402">🔑 id (PK)</text>
  <text x="269" y="430" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#BA7517">🔗 animal_id (FK)</text>
  <text x="269" y="448" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#BA7517">🔗 veterinario_id (FK)</text>
  <text x="269" y="466" dominant-baseline="central" font-size="11" font-family="sans-serif" fill="#412402">data_consulta, motivo...</text>

  <!-- Relações -->
  <line x1="205" y1="100" x2="255" y2="100" stroke="#888" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="230" y="90" text-anchor="middle" font-size="11" font-family="sans-serif" fill="#555">1 : N</text>

  <line x1="342" y1="290" x2="342" y2="360" stroke="#888" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="360" y="328" font-size="11" font-family="sans-serif" fill="#555">1 : N</text>

  <path d="M562 270 L562 430 L430 430" fill="none" stroke="#888" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="548" y="315" text-anchor="middle" font-size="11" font-family="sans-serif" fill="#555">1 : N</text>

  <!-- Legenda -->
  <rect x="30" y="460" width="210" height="48" rx="6" fill="#f9f9f9" stroke="#ddd" stroke-width="0.5"/>
  <text x="44" y="478" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#333">🔑 PK — Chave Primária</text>
  <text x="44" y="498" dominant-baseline="central" font-size="12" font-family="sans-serif" fill="#BA7517">🔗 FK — Chave Estrangeira</text>
</svg>
