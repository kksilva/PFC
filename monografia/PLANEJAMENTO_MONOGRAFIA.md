# Plano de Conteúdo da Monografia — Checklist Completo

Organizado conforme a estrutura do `Monografia.tex` (modelo PFC/UFMG em LaTeX/ABNT).
Legenda de status: **[OK]** já existe material pronto (relatórios/dados) · **[PARCIAL]** existe, precisa adaptar · **[PENDENTE]** depende do ensaio definitivo ou escrita nova.

---

## Resumo (NBR 6028)

**[PARCIAL]** Rascunho já aprovado pelo usuário (versão enxuta, ~150 palavras).
- [x] Problema: malha aberta vs. PSR (seguimento de referência) e PRP (rejeição de perturbações)
- [x] Objetivo: curva torque × corrente do Kyosho Mad Force Kruiser 2.0 VE
- [x] Método em 2–3 frases (ACS758 + Due, degraus via Raspberry Pi, balança)
- [ ] Resultados numéricos finais: placeholders `[X]%`, `[I₁]–[I₂] A` → preencher com ensaio definitivo
- [x] Palavras-chave (6 termos)

## Abstract

**[PENDENTE]** Tradução fiel do resumo fechado. Keywords em itálico, ordem alfabética.

## Agradecimentos

**[PENDENTE]** Texto curto e pessoal (família, orientador, colegas de laboratório). Escrever por último.

## Lista de Figuras / Lista de Tabelas / Sumário

**[OK]** Geradas automaticamente pelo LaTeX a partir dos `\label{}`. Nada a escrever — só garantir que toda figura/tabela tenha legenda (`\caption`).

---

# CAPÍTULO 1 — Introdução

**[PARCIAL]** Conteúdo-base: Proposta de Projeto v2 e Relatório Parcial 1.

- [ ] **1.1 Contextualização**
  - Automodelismo elétrico 1/8; o Kyosho Mad Force Kruiser 2.0 VE como plataforma (motor Orion 2100 KV, ESC Orion R8)
  - Acionamento em malha aberta: piloto → rádio → ESC → motor; ausência de realimentação
  - Competições PSR/PRP da RoboCore/CTE: necessidade de trajetórias suaves e reproduzíveis
  - Ligar ao problema de controle: PSR (seguimento de referência) e PRP (rejeição de perturbações) — definições corretas conforme Proposta v2
- [ ] **1.2 Problema de pesquisa**
  - Como estimar o torque entregue pelo powertrain embarcado, de baixo custo, sem dinamômetro comercial?
- [ ] **1.3 Objetivos**
  - Geral: caracterizar a curva torque × corrente e validar a estimativa indireta de torque via corrente
  - Específicos: (i) instrumentar o veículo com ACS758; (ii) desenvolver método de ensaio travado com balança; (iii) validar contra modelo teórico com redução i ≈ 11,5; (iv) quantificar erros e incertezas
- [ ] **1.4 Justificativa**
  - Dinamômetros comerciais caros e inviáveis embarcados; sensor de corrente de efeito Hall é barato e já isolado galvanicamente
  - Contribuição para controle em malha fechada futuro (controlador de aceleração)
- [ ] **1.5 Organização do trabalho** (1 parágrafo por capítulo)

# CAPÍTULO 2 — Descrição do Processo

**[PARCIAL]** Conteúdo-base: Relatórios Parciais 1, 2 e 3 + datasheet ACS758 + manual Kyosho.

- [ ] **2.1 O automodelo e seu powertrain**
  - Motor brushless Orion 2100 KV (princípio BLDC, KV = rpm/V), ESC Orion R8 (120 A contínuos / 760 A pico)
  - Transmissão 4WD por corrente; redução total i ≈ 11,5 (valor medido pelo orientador — citar)
  - Bateria LiPo 2S 7,4 V 5200 mAh: cuidados, C-rate, ciclos de vida, **efeito "sag"** (queda de tensão sob carga) — ver item 2.6
- [ ] **2.2 Sinal de comando (PWM/servo)**
  - Padrão de pulso 90–180° (mapa do PCA9685), neutro em 95°, possibilidade de ré em 90–94°
  - Raspberry Pi + PCA9685 como gerador de degraus reproduzíveis
- [ ] **2.3 Sensor de corrente ACS758 (datasheet)**
  - Efeito Hall, isolamento galvânico, faixa ±200 A, sensibilidade 10 mV/A (5 V), largura de banda 120 kHz, ruído 3 mV, não-linearidade ±1%
  - Saída ratiométrica: offset = 50% da alimentação (Vq = 1,65 V a 3,3 V; sensibilidade efetiva 6,6 mV/A) — **este é o estudo da "nova" alimentação a 3,3 V, que substitui o esquema antigo de 7805 + divisor**
  - Necessidade de calibração do offset no código
- [ ] **2.4 Arduino Due**
  - ADC de 12 bits (resolução ~0,8 mV ≈ 0,12 A), alimentação lógica 3,3 V nativa (compatível com o ACS758), leitura serial → Python
- [ ] **2.5 Relação corrente de bateria × torque (modelo teórico)**
  - I_fase ≈ I_bateria / D (duty cycle), I_fase → torque eletromagnético ∝ I_fase; modelo global T(I_bateria) esperado linear
  - Papel da redução i ≈ 11,5: torque no eixo das rodas = i × torque do motor (desprezando perdas)
- [ ] **2.6 Estudo da bateria — seção obrigatória (lição aprendida)**
  - LiPo "estufada"/gasta → LVC do ESC (LED piscando, perda de força sob carga)
  - **Sag**: tensão cai sob corrente alta → duty efetivo cai → "degraus que encolhem" na série (ex.: degrau 114 executado com força de degrau menor)
  - Consequência: séries medidas com bateria gasta foram **descartadas**; método de controle de saúde da bateria (verificar tensão por célula, descartar estufadas, pausas de 60 s entre degraus para recuperação)
  - Incluir: ensaio definitivo deve registrar tensão da bateria (ou ao menos estado de carga) por série
- [ ] **2.7 Fundamentos de controle**
  - PSR/PRP, malha aberta × fechada, por que torque estimado habilita o controlador futuro

# CAPÍTULO 3 — Metodologia

**[PARCIAL]** Conteúdo-base: Relatório Experimental + prática de bancada consolidada neste projeto.

- [ ] **3.1 Escolha da instrumentação (seção nova, solicitada)**
  - Por que balança digital de mala e não torquímetro/dinamômetro comercial (custo, disponibilidade, rastreabilidade da comparação 5,140 vs 5,130 kg)
  - Por que ACS758 (faixa cobre picos do ESC, isolamento, baixo custo) vs. shunt (perda, sem isolamento) vs. SCT013 (faixa/banda inadequadas)
  - Por que Arduino Due (ADC 12 bits, 3,3 V nativo) vs. Uno/Nano (10 bits, 5 V exigiria divisor — esquema descontinuado)
  - Por que Raspberry Pi + PCA9685 para os degraus (reprodutibilidade, não mexer no rádio original)
  - **Figura:** diagrama em blocos: Pi → PCA9685 → ESC → motor → transmissão → rodas; bateria → ACS758 → Due → PC; balança → registro manual
- [ ] **3.2 Montagem do ensaio travado**
  - Veículo apoiado no chão (superfície onde será usado), ancoragem pela balança entre gaveta/estrutura fixa e o veículo
  - **Balança suspensa pela alça** → linha de tração horizontal → θ ≈ 0 por construção (decisão final que elimina a medição/correção de θ)
  - Massa adicional sobre o veículo: **função dos pesos** — aumentar aderência/normal (N = m·g, atrito disponível) para evitar patinagem; é condição de ensaio documentada, NÃO entra no cálculo do torque (T = F × R_ef independe da massa); mencionar patinagem observada (carro "levantando" na suspensão sob torque) e como a massa mitigou
  - Taragem da balança 1× por série, em repouso, nunca entre degraus
- [x] **3.3 Interferência do ângulo θ (RESOLVIDO — decisão 22/10/2026: θ desprezível, sem correção)**
  - Erro cos θ na medida: F_medida = F_real × cos θ
  - Montagem final: balança **suspensa pela alça** entre armário (ancoragem) e gancho no para-choque — a suspensão alinha o eixo do instrumento à linha de tração (sem erro interno de alinhamento)
  - O θ residual depende só da geometria dos pontos de engate: θ = arctan(|h1 − h2| / L). Como a balança pende livre, a linha de tração permanece horizontal enquanto os pontos estiverem em alturas próximas — erro < 0,5% mesmo com Δh de alguns cm em L ≈ 1 m
  - Evidência: 5,140 kg (vertical) vs. 5,130 kg (horizontal) = 0,19% < resolução da balança (10 g)
  - Redação para a monografia: declarar θ desprezível com justificativa em 2 níveis (suspensão pela alça + geometria de engate) — sem correção trigonométrica aplicada
- [ ] **3.4 Procedimento do ensaio**
  - Escada de degraus: subida 95→115° (rodar_ensaio.py) e descida 115→95° (rodar_ensaio_desc.py), passo 1°, duração 10 s por degrau, pausa 60 s
  - Janela de leitura: últimos 3 s (7–10 s) para amortecer transientes — **função da pausa/janela**: deixar o transiente mecânico dissipar e evitar o sag cumulativo da bateria
  - Sincronização: `proc.wait(timeout=20)` + folga de 3 s para o Due não dessincronizar do Pi
  - Leitura de corrente: Python (`leitura.py`) registrando CSV `t_ensaio; t_degrau; ângulo; corrente` (aberto com `open("x")` — nunca sobrescreve ensaio anterior)
  - Repetições: ≥3 séries (subida + descida) para repetibilidade e histerese
- [ ] **3.5 Validação teórica**
  - Comparação degrau a degrau: torque medido (T = F × R_ef, R_ef = 0,08 m) × i vs. torque eletromagnético estimado a partir de I_fase ≈ I_bateria/D
  - Critério: desvio < 5% nos degraus onde o modelo linear de duty é válido (excluir 100–102°, onde D = (θ−95)/85 falha perto do neutro)
  - Tratamento do "peso de retorno elástico" (coluna F do xlsx, 120–355 g): diagnóstico de creep/retorno do conjunto, não entra na regressão
- [ ] **3.6 Incertezas e tratamento de erros**
  - Resolução balança (10 g ≈ 0,008 N·m), resolução ADC (0,12 A), modelo linear de duty perto do neutro, patinagem residual, sag da bateria
  - Tabela de incertezas propagadas em T

# CAPÍTULO 4 — Resultados

**[PARCIAL]** Dados atuais: "subida 1" (9 degraus, 97–115°, I de 0,6 a 18,3 A).

- [ ] **4.1 Ensaio preliminar (subida 1)**
  - Tabela: degrau (°) | I média (A) | F (gf) | T (N·m) | desvio modelo (%)
  - Regressão T = 0,185·I + 0,48 (r = 0,92) na janela 7–10 s
  - **Figura:** gráfico torque × corrente com barras de incerteza
  - Análise degrau a degrau: concordância <5% em 104–115° (115° = 0,0% exato); 100–102° desviam ~−47% (modelo de duty falha no neutro) → exclusão justificada; ponto 108° defeituoso (força caiu) → descarte justificado
  - **Fato-chave:** força não saturou em 115° → escada deve estender até ~130° no ensaio definitivo
- [ ] **4.2 Ensaio definitivo [PENDENTE — requer LiPo 2S saudável 5200 mAh]**
  - Escada estendida até saturação (~130°), 21+ degraus, passo 1°
  - Subida + descida (histerese)
  - ≥3 repetições (média e desvio-padrão por degrau)
  - Ensaio em vazio (sem aceleração) por degrau → I₀ e "tara" de corrente
  - Registrar tensão de bateria por série (controle do sag)
- [ ] **4.3 Análise comparativa**
  - Tabela final consolidada; regressão definitiva T(I) com r e incerteza dos coeficientes
  - Histerese subida × descida (atrito/seco vs. região de escorregamento do ESC)
  - Repetibilidade (desvio-padrão relativo por degrau)
  - Comparação final com modelo teórico (desvio % por degrau e global)
- [ ] **4.4 Discussão das fontes de erro** (síntese do estudo da bateria + θ + patinagem + modelo de duty)

# CAPÍTULO 5 — Conclusão

**[PENDENTE]** Escrever com os resultados definitivos.

- [ ] Considerações finais: método validado (ou limitações), concordância com modelo, resposta ao problema de pesquisa
- [ ] Limitações: ensaio travado (não dinâmico), bateria, aderência, aproximação I_fase ≈ I_bat/D
- [ ] Propostas futuras: controle em malha fechada em movimento (controlador real), ensaio dinâmico, proteção por corrente embarcada, estimativa de μ/patinagem

# Referências Bibliográficas

**[PARCIAL]** `ListadeReferencias.bib` já tem 9 refs. Garantir citação de todas no texto (ABNT: toda entrada citada, toda citação na lista). Adicionar: datasheet ACS758 (Allegro), manual Kyosho, docs Arduino/PCA9685 se usados.

# APÊNDICE A — Códigos

**[OK]** Código Arduino `.ino` (versão final corrigida: offset e sensibilidade 3,3 V) e scripts Python (`leitura.py`, `rodar_ensaio.py`, `rodar_ensaio_desc.py`). Listar integralmente com `\lstlisting` ou verbatim.

# APÊNDICE B — Datasheet e registros

**[PARCIAL]** Folha de dados ACS758XCB, tabela completa dos CSVs de ensaio (ou indicação do repositório GitHub kksilva/PFC), planilha de ensaio (`planilha_ensaio.xlsx`) como registro de campo.

# Capa

- [ ] **[PENDENTE]** Substituir `[Nome do Orientador]` pelo nome real.

---

## Itens transversais (não esquecer)

1. Toda figura com `\caption` + `\label` (alimenta lista de figuras)
2. Todas as tabelas com legenda (lista de tabelas)
3. Citações ABNT: `\cite{}` para todas as refs
4. Compilar no Overleaf (upload da pasta `monografia/`) — LaTeX local não testado
5. Repositório: `github.com/kksilva/PFC` já sincronizado; atualizar a cada sessão
6. Nomenclatura: PSR = Problema de Seguimento da Referência; PRP = Problema de Rejeição de Perturbações (NÃO é "percurso de solo")
7. Datas: defesa PFC II prevista 15–19 jun 2026 — ensaio definitivo deve acontecer com folga
