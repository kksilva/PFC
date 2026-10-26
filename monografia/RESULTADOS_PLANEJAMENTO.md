# Planejamento de Escrita — Capítulo 4 (Resultados) — v2

Comentários da autora incorporados (26/10). Decisões estruturais novas:
1. **As regiões de operação são definidas na abertura do capítulo** (4.1) e nomeadas uma única
   vez — o resto do texto trabalha com os NOMES (zona morta, aderência, saturação), não com
   faixas de números repetidas. É a principal medida contra a densidade.
2. **Um número só aparece uma vez** — na tabela-mestra ou na figura. A prosa discute padrões e
   interpretações; não reenumera valores.
3. **Tudo que envolve controlador (variáveis, estrutura, onde cada ensaio entra, implicações)
   migra para o Capítulo 5**, que ganha um bloco próprio "Estrutura da malha de controle" antes
   da sintonização. O Cap. 4 termina no que foi medido; o Cap. 5 diz o que se faz com isso.
4. **Explicações didáticas embutidas** (r², η, regressão, stick-slip etc.) entram como frases
   de apoio no fluxo — lista no final deste arquivo.

Fatos confirmados pela autora:
- Vazio: escala 97→117→97→117 — **duas subidas completas e uma descida** (primeira varredura
  do 97° descartada por dessincronização). No texto: não detalhar; apenas consolidar.
- Tração 100 Hz: arquivo ensaio_cego_subida; **contar e tratar os inválidos sem especificar o
  critério no texto** (o critério já está na 3.5).
- μ = 0,80 e η/r²: sem ferramentas de confirmação — escrever os valores e **discutir a
  plausibilidade com justificativa física** (condizente ou não, e por quê).

---

## 4.1 Regiões de operação e tabela-mestra
- **Abertura**: o capítulo organiza os resultados pelas regiões que o ensaio revelou, definidas
  aqui com seus nomes e limites (FIGURA 4.1 — força × comando com as regiões sombreadas):
  - **zona morta** (97–99°): ESC armado, corrente residual, sem tração útil;
  - **região de aderência** (100–113°): roda travada, força segue o comando — região válida
    para o modelo linear e para o controlador;
  - **região de saturação** (>113–114°): aderência esgotada, patinagem/corte do ESC — fora do
    modelo linear.
- **TABELA 4.1 (mestra)**: degrau | u | I_sub | F_sub | I_desc | F_desc (médias de 4 rep.,
  dp entre parênteses). Aparece UMA vez; o resto do capítulo referencia a tabela e as regiões.
- Localização da tabela: **corpo do texto** (é a evidência central) — decisão da autora [OK?].

## 4.2 Ensaio em Vazio
- I₀(u) × u (FIGURA 4.2) com ajuste linear I₀ = 0,54 + 9,36u (r² = 0,97).
- Frase de apoio: o que é r² (proporção da variância explicada pelo ajuste) — explicação curta.
- O que o resultado significa: corrente de perdas cresce linearmente com o comando → duas
  funções (alimenta o modelo 4.4; evidencia linearidade do ESC).
- Tratamento dos descartes: justificativa (pico < 1 A = comando não executado; se mantidos,
  distorceriam a média) — uma frase, sem detalhar critério.

## 4.3 A Curva Característica (força × comando)
- Narrativa **por região** (usando os nomes da 4.1), com a figura à frente:
  - zona morta: força residual ~0,45 kgf;
  - aderência: força cresce com o comando, subida e descida;
  - saturação: patinagem na subida com pneu frio (força estaciona ~3,2–3,3 kgf enquanto a
    corrente oscila) vs. descida estável até 5,32 kgf (pneu aquecido);
  - faixa extrema: colapso de corrente e força observado nos degraus finais da descida
    (comportamento de corte cíclico do ESC) — registrado como observação, não como ponto.
- **Histerese em uma figura só** (laço subida×descida) + um parágrafo: diferenças +7 a +45%,
  interpretação = memória térmica do pneu (μ sobe com a temperatura), NÃO histerese do
  powertrain. Definir stick-slip aqui (primeira ocorrência).

## 4.4 Validação do Modelo Torque × Corrente
- Estimador na forma de trabalho: T̂ = C·(I − I₀(u))/u, com C = η·i·K_t/r_ef condensado —
  **uma constante do conjunto** (resposta ao "não tem forma simplificada?").
- Como se valida: regressão sem intercepto de y = F·r_ef·u/(K_t·i) contra x = (I − I₀) —
  explicar em uma frase o raciocínio (se o modelo é verdadeiro, y deve ser proporcional a x,
  passando pela origem; o slope é η).
- Resultados por sentido, SEM repetir números em prosa — tabelinha ou inline mínimo:
  descida η = 0,579, r² = 0,962 (valida); subida η = 0,596, r² = 0,784 (stick-slip).
- η: o que representa (rendimento global do powertrain no ponto de operação) e como entra no
  modelo do controlador (o ganho do feedforward — remeter ao Cap. 5, sem detalhar).
- K_t efetivo 2,5–2,7 mN·m/A = 4,55·η: coerente; **não valida o 2100 KV isolado** porque η e
  K_t aparecem multiplicados — separá-los exigiria medir a rotação (proposta de continuidade).
- Validade limitada à região de aderência: acima dela, a corrente deixa de determinar a força
  (patinagem) e o formalismo I/u deixa de representar a corrente de fase (D ≠ u) — o que é
  isso: o ESC não entrega mais o duty nominal sob corte/patinagem.
- μ aparente ≈ 0,80 (52 N sobre 65,1 N): discutir plausibilidade — condizente com borracha de
  automodelo em piso seco COM transferência de carga (dianteira descarrega, traseira carrega);
  sem a transferência, μ > 1 seria exigido, o que seria incompatível.
- Torque máximo ≈ 3,9 N·m (um número, na tabela ou aqui — uma vez só).

## 4.5 Dinâmica Comando → Corrente
- Bordas de subida da região de aderência (100–109°): método da 63,2% + LSQ (o que cada um é,
  uma frase). Bordas acima de 110° não usadas: resposta contaminada pela patinagem.
- Resultados: K = 116–125 A/u (confirma o estático); θ < 0,1 s; τ = 1,8–2,0 s.
- **Achado e implicação (explicada)**: o prior clássico (L/R do motor, milissegundos) não se
  aplica; a dinâmica é do ESC (rampa interna de corrente). Implicação para controle: a planta é
  LENTA — o controlador não pode ser mais rápido que ela (λ ≥ 0,25τ) — remeter ao Cap. 5.
- Consequência prática já verificada no protocolo: regime em ~4τ ≈ 7 s (janela de anotação
  validada retroativamente).
- FIGURA: respostas ao degrau sobrepostas com o ajuste.

## 4.6 Incertezas dos Resultados
- TABELA 4.2 (eu gero de `pfc kaka.xlsx`): u_A entre escadas por faixa; u_B; U(T) = 2u_c.
- Estimativa de trabalho: repetibilidade ±50 g → U(T) ≈ ±0,09 N·m na faixa alta.

## 4.7 Limitações
- Sem dinâmica u→F (força só em platô anotado; continuidade = célula de carga com registrador);
- aquisição contínua com lacunas de rede e descida incompleta;
- faixa extrema contaminada pelo corte do ESC;
- K_t do datasheet não isolado (sem rotação);
- dinâmica identificada só na região de aderência.

## Resumo do Capítulo
Quatro entregas nomeadas: corrente de perdas I₀(u); curva característica por regiões; modelo
validado (η, r²) e sua fronteira de validade; dinâmica identificada (τ, θ) com o prior refutado.
Uma frase: "sobre esses resultados estrutura-se a malha de controle, objeto do Capítulo 5."

---

## Escopo do Capítulo 5 (a escrever depois, conforme pedido da autora)
Seção única "Estrutura da malha de controle" ANTES da sintonização, descrevendo:
- **Variáveis lidas embarcado**: u (comando, conhecido) + I_bat (ACS758) → T̂ estimado;
- **Onde cada ensaio entra**: I₀(u) do vazio → subtrator do estimador/feedforward; curva
  estática T×I → inversa (feedforward) e limitador de aderência; G₁(s) do ensaio 100 Hz →
  projeto do PI;
- **Arquitetura**: malha interna de corrente (PI sobre G₁) + feedforward de inversa estática +
  limitador T_max (limiar de aderência) + anti-windup + rate-limit;
- **Por que corrente e não força na realimentação**: força não é mensurável online (balança só
  tem display) — a malha fecha em corrente e estima torque;
- **O que NÃO fecha**: validação experimental da malha (sem dinâmica u→F) = continuidade.
- Então a sintonização: PI-IMC com τ, θ medidos; λ = 0,6 s; simulação PSR/PRP + robustez.

---

## Explicações didáticas a embutir (uma frase cada, no ponto da primeira ocorrência)
- r²: fração da variância dos dados explicada pelo ajuste; 1 = perfeito.
- Regressão sem intercepto da validação: se o modelo é exato, y ∝ x pela origem; slope = η.
- η: rendimento global medido (elétrico→mecânico) do powertrain no ponto de operação.
- Stick-slip: oscilação de relaxamento do atrito seco no limite de aderência.
- Método da 63,2%: tempo em que a resposta atinge 63,2% do valor final ≈ τ (com θ ≈ 0).
- LSQ: mínimos quadrados — ajuste que minimiza a soma dos quadrados dos resíduos.
- Transferência de carga: sob aceleração, o peso migra do eixo dianteiro para o traseiro,
  aumentando a aderência disponível nas rodas motrizes.

## Ordem de escrita
1. 4.1 (regiões + tabela-mestra) — eu gero a tabela;
2. 4.5 (dinâmica);
3. 4.4 (validação);
4. 4.3 (curva);
5. 4.2 (vazio);
6. 4.6 (tabela de incertezas — eu gero);
7. 4.7 + Resumo.
