# Planejamento de Escrita — Capítulo 4 (Resultados)

O capítulo segue a **mesma ordem dos experimentos do Capítulo 3** (bancada → vazio → tração),
para o leitor atravessar os dois capítulos no mesmo ritmo. Cada seção de resultado abre com o
que o ensaio correspondente prometia e fecha com o que ele entregou. **Confira os fatos
marcados [ ] e corrija o que mudou.**

Fatos já fechados (da análise de 26/10, `ensaios/pfc kaka.xlsx` + consolidado + vazio):
- Vazio: I₀(u) medido, 97°→0,49 A ... 117°→2,84 A; ajuste I₀ = 0,54 + 9,36·u (r² = 0,97).
- Tração (força, 4 repetições por sentido, subida 97→117 / descida 117→97):
  força máxima 5,32 kgf (52 N) em 114° descida; saturação ~3,2–3,3 kgf na subida 105–110°;
  colapso de corrente e força em 116–117° descida (corte cíclico do ESC); zona morta 97–99°.
- Validação do modelo: η = 0,579 (r² = 0,962, n = 56, descida 100–113°); η = 0,596
  (r² = 0,784, n = 44, subida 100–110°); K_t efetivo 2,5–2,7 mN·m/A (= 4,55·η).
- Dinâmica (cego 100 Hz): K = 116–125 A/u; θ < 0,1 s; τ = 1,8–2,0 s (LSQ reparte
  θ~1,0 + τ~1,0; usar a soma); prior da literatura refutado (ESC domina).
- Massa do conjunto: 6,640 kg → μ aparente = 52/(6,64·9,81) ≈ **0,80** (era 0,75 com 7,1 kg).

---

## 4.1 Ensaio em Vazio — [OK?]
- **O que prometia (Cap. 3):** I₀(u), a corrente de perdas por comando.
- **Resultado:** tabela ou figura de I₀ × degrau (97→117°); valores de 0,49 a 2,84 A;
  linearidade do ESC evidenciada pelo ajuste I₀(u) = 0,54 + 9,36u, r² = 0,97.
- **Tratamento:** descarte de execuções dessincronizadas (pico < 1 A em varreduras específicas).
- **Papel no modelo:** subsidia a subtração (I − I₀) da validação (4.2).
- FIGURA: I₀(u) × u com o ajuste linear.

## 4.2 Ensaio de Tração Estática — [OK?]

### 4.2.1 A curva força × comando
- Pontos subida/descida (médias de 4 repetições, barras de erro da repetibilidade — TABELA/FIGURA).
- Leitura em blocos:
  (a) **zona morta** 97–99° (corrente 0,5–1,3 A, força residual ~0,45 kgf);
  (b) **região de aderência** 100–110°: força cresce com o comando;
  (c) **saturação aparente na subida** 105–110° (~3,2–3,3 kgf, pneu frio, stick-slip);
  (d) **faixa alta**: força até 5,32 kgf (114° descida);
  (e) **colapso em 116–117° na descida** — corrente e força caem (corte cíclico do ESC por
      subtensão; relato "engasga e volta") — declarar como comportamento observado, não como
      ponto da curva.
- **Histerese:** descida acima da subida em +7 a +45% (104–115°) — interpretação: memória
  térmica do pneu (descida com pneu aquecido adere sem stick-slip; corrente sustentada maior).
  NÃO é histerese do powertrain. [OK?]

### 4.2.2 Validação do modelo torque × corrente
- Estimador: T̂ = η·i·K_t·(I − I₀(u))/(u·r_ef) (equação já na 2.1/2.3 — referenciar, não repetir).
- Regressão sem intercepto y = F·r_ef·u/(K_t·i) × x = (I − I₀): η e r² por sentido.
- **Descida valida** (r² = 0,962); subida mais dispersa (r² = 0,784) — explicação do stick-slip
  (força presa no limite de aderência, corrente oscilando; pneu frio).
- K_t efetivo 2,5–2,7 = 4,55·η — coerente, mas **não valida o 2100 KV isoladamente**
  (falta rotação medida — declarar).
- Validade limitada a ≤113–114°: η > 1 acima (D ≠ u na saturação).
- μ aparente ≈ 0,80 (52 N sobre 65,1 N do conjunto 6,640 kg) com transferência de carga.
- Torque máximo: T = 52 × 0,0751 ≈ 3,9 N·m.

## 4.3 Dinâmica Comando → Corrente — [OK?]
- Fonte: ensaio cego 100 Hz (retemo por índice, Cap. 3).
- Bordas de subida 100–109°: método da 63,2% + LSQ; K = 116–125 A/u confirma o estático (120).
- θ < 0,1 s (resposta inicia na primeira janela); τ = 1,8–2,0 s.
- **Achado:** prior clássico (L/R em ms) refutado; dinâmica dominada pelo escalonamento interno
  do ESC (soft-start/punch, partida sensorless travada).
- Consequência prática verificada: platô em ~4τ ≈ 7 s — a janela de anotação (s 7–9) estava
  correta; consequência para o controlador (λ) remete ao Cap. 5.
- Cautelas: borda do 110° cortada; par (θ, τ) mal-condicionado (usar a soma).
- FIGURA: respostas ao degrau sobrepostas com o ajuste FOPDT.

## 4.4 Incertezas dos Resultados — [falta gerar tabela]
- Tipo A: repetibilidade das 4 escadas (desvio-padrão por degrau — **gerar da planilha**);
  dispersão das 3 leituras 7–9 s (se guardadas; senão, só entre-escadas).
- Tipo B e sistemáticas: já orçados na 3.5 — aqui apenas propagar até T = F·r_ef e dar
  U(T) por faixa. **TABELA a gerar** (`pfc kaka.xlsx`).
- Estimativa inicial: ±50 g de repetibilidade → u_c(F) ≈ 50 g → U(T) ≈ ±0,09 N·m na faixa alta.

## 4.5 Limitações — [OK?]
- Sem dinâmica u→F (célula de carga com registrador = continuidade);
- descida 98–112° só sem força (aquisição contínua) / lacunas de rede;
- 116–117° contaminados pelo corte do ESC;
- K_t do datasheet não isolado (sem rotação);
- dinâmica identificada só na região de aderência.

## Resumo do Capítulo
Fecho em quatro entregas: I₀(u) medida; curva torque×corrente validada (η, r²); dinâmica
identificada (τ, θ) com prior refutado; confiança quantificada. Ponte ao Cap. 5.

---

## Pontos que preciso que você confirme antes de escrever
1. **[ ]** O ensaio em vazio usou exatamente a escala 97→117° (sem descida)? Quantas repetições?
2. **[ ]** A tabela mestra da curva força×comando (degrau, I, F, subida/descida, 4 rep.) entra
   no apêndice ou no corpo? Recomendo: corpo (Tabela) nas faixas-chave + apêndice completo.
3. **[ ]** Resultados preliminares antigos (ensaio com EVA, T = 0,185·I + 0,48, r = 0,92,
   faixa 3,6–18,2 A): incluir como 4.1 "resultados preliminares" ou descartar? [sugerido:
   descartar do corpo, citar só na introdução dos resultados como motivação]
4. **[ ]]** μ = 0,80 confirmado com a massa 6,640 kg?
5. **[ ]** Os valores de η e r² por sentido estão conforme a análise (0,579/0,962 e
   0,596/0,784)?

## Ordem de escrita proposta
1. 4.3 (dinâmica) — bloco fechado e independente;
2. 4.2.2 (validação) — números prontos;
3. 4.2.1 (curva) — precisa decidir tabela vs figura;
4. 4.1 (vazio) — curto;
5. 4.4 — eu gero a tabela de incertezas antes;
6. 4.5 + Resumo.
