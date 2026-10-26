# Planejamento de Escrita — Capítulo 3 (Metodologia) — v4

Fatos confirmados pela autora (26/10, noite):
- Cabo de 126 cm de cada lado da balança; balança a 15 cm do chão; engate a 28 cm do chão;
  3× cada → sen θ = 13/126 → θ = 5,9°; cos θ = 0,995 (correção ≤ 0,53%).
- Gancho engatado em estrutura traseira do veículo, ACIMA do eixo de transmissão.
- Tara nos 3 s de neutro entre degraus; força anotada nos segundos 7, 8 e 9; ponto = média
  dos 3; idem na descida; sessão gravada em vídeo e lida quadro a quadro depois.
- Massa total: 6,640 kg (3×). [efeito: μ do Cap. 4 = 0,80]
- Sensor: ACS758ECB-200B (±200 A) a 3,3 V → 6,6 mV/A; offset 1,65 V; ADC 12 bits →
  122 mA/LSB (u_B ≈ 35 mA).
- Script de degraus (`teste_throttle.py`) disponibilizado pelo orientador; executa no
  Raspberry Pi, acionado por ssh do notebook: `ssh alunos@raspberrypi.local
  "python3 teste_throttle.py <ângulo> <duração>"`.
- **Verificação em bancada do sensor**: corrente lida no multímetro de referência e no
  ACS758; relação linear em toda a faixa 0–6 A; regressão y = 1,0742x; desvios sistemáticos
  de ±7% compensáveis por fator de correção em software.
- Escadas: (a) com força + vídeo — subida 97→117°, descida 117→97°; (b) aquisição contínua
  100 Hz — subida 98→119°, descida 120→113°.

---

## 3.1 Princípio do Ensaio de Tração Estática e Montagem

**P1 (abertura).** Caracterizar o propulsor exige medir força de tração e corrente
simultaneamente. A força só se manifesta em movimento; o ensaio ancorado a mede em condição
estacionária: o veículo é impedido de se deslocar e a reação da ancoragem iguala a tração,
dispensando dinamômetro. Fecho: o torque na roda segue T_roda = F·r_ef (§3.3).

**3.1.1 Configuração de ancoragem — 2 parágrafos.**
- P1: gancho da balança engatado na estrutura traseira do veículo, acima do eixo de
  transmissão; cabo de 126 cm em cada lado da balança; balança suspensa — 15 cm do chão no
  lado do padrão e 28 cm no engate; dimensões anotadas 3×.
- P2: essa geometria define o ângulo do cabo, tratado na Seção 3.2.
- FIGURA: fotografia da montagem.

**3.1.2 Padrão de força e registro em vídeo — 2 parágrafos.**
- P1: balança digital de mala com gancho, resolução 10 g; alternativas rejeitadas
  (dinamômetro comercial — custo; célula de carga com registrador — proposta de continuidade,
  viabilizaria a medição dinâmica da força).
- P2: sessão gravada em vídeo; cada ponto lido pausado, quadro a quadro, após o experimento —
  padroniza a leitura, elimina erro de pressa e paralaxe, e dá rastreabilidade; o display não
  possui saída elétrica.

**3.1.3 Massa adicional — 1 parágrafo.** Conjunto a 6,640 kg, anotado 3×; função
exclusivamente condicionante (aumenta a carga normal e o atrito disponível, retardando a
patinagem); não entra no cálculo do torque; a condição de carregamento integra a especificação
do ensaio.

## 3.2 Geometria do Cabo e o Efeito Cosseno — 2 parágrafos

- P1: a balança mede a tensão no cabo; interessa a componente na linha de tração, F·cos θ;
  das dimensões medidas (3×): sen θ = (28−15)/126 → θ = 5,9° → cos θ = 0,995 → correção
  máxima de 0,53%, inferior à incerteza de leitura — θ desprezado por medida.
- P2 (verificação independente): o peso do veículo medido na vertical (5,140 kg, sem a massa
  adicional) e na horizontal, com o cabo esticado ao máximo, concordam dentro de 0,2% — a
  montagem não introduz componente vertical mensurável.

## 3.3 Medida do Raio Efetivo da Roda — 1–2 parágrafos

Método roll-out: marcas no pneu e no solo; a roda é movimentada 5 vezes com o veículo
encostado na parede, o que garante o rolamento reto; 3 anotações independentes; L = 236 cm →
r_ef = L/(2π·5) = 0,0751 m, contra 80 mm nominais (pneu novo, sem carga) — deflexão de 6,1%
sob carga. Usa-se r_ef em T = F·r_ef: o raio nominal injetaria 6% de erro sistemático.

## 3.4 Instrumentação e Aquisição de Dados

**3.4.1 Medição da corrente — 3 parágrafos.**
- P1 (o sensor): ACS758ECB-200B em série na alimentação do conjunto ESC–motor; sensor de
  efeito Hall, isolado galvanicamente; alimentado a 3,3 V pelo Arduino Due; sensibilidade
  ratiométrica de 6,6 mV/A a 3,3 V (10 mV/A a 5 V) e saída de 1,65 V em corrente zero; filtro
  RC de ~24 Hz na entrada; ADC de 12 bits → resolução de 122 mA por LSB.
- P2 (a verificação em bancada): antes do ensaio, o sensor foi verificado em bancada contra
  um multímetro de referência, com fonte de 0 a 6 A; a resposta foi linear em toda a faixa,
  com regressão y = 1,0742x entre multímetro (x) e sistema (y); os desvios sistemáticos de
  ±7% são compensáveis por fator de correção em software — o sensor fica validado para o
  monitoramento da corrente.
- P3 (os dois firmwares): firmware básico — 100 amostras ADC consecutivas (~1 ms) por ponto,
  1 ponto/s (ensaio com forças); firmware rápido — período de 10 ms, ~100 Hz (aquisição
  contínua). Regras de amostragem (10–30× a banda) — reativar citações depois.

**3.4.2 Aquisição a 100 Hz — 1 parágrafo.** As amostras chegam pela serial em rajadas de ~10
com o mesmo timestamp (blocos de 100 ms); a ordem serial preserva a sequência, de modo que o
retempo é feito por índice, t = k×10 ms; cada degrau de 15 s gera ~1550 amostras. Reconstrói-se
o tempo sem perda de resolução.

**3.4.3 Geração dos degraus e registro em CSV — 2 parágrafos.**
- P1 (o comando): o script de comando dos degraus foi disponibilizado pelo orientador e
  executa no Raspberry Pi; o notebook o aciona remotamente por ssh, na forma
  `ssh alunos@raspberrypi.local "python3 teste_throttle.py <ângulo> <duração>"`; o script
  coloca o ESC em neutro (95°), aplica o degrau pela duração programada e retorna ao neutro.
  O gerador de pulsos (PCA9685) opera na faixa padrão de servo, 90–180°, com comando
  normalizado u = (θ−95)/85.
- P2 (a aquisição): um script de automação local percorre a escala de degraus em um laço,
  substituindo o ângulo e a duração a cada iteração e lançando o comando ssh correspondente;
  em paralelo, a serial do Arduino é lida continuamente e cada amostra — tempo de ensaio,
  tempo dentro do degrau, ângulo e corrente — é registrada em arquivo CSV, um bloco por
  degrau. O resultado é a série temporal completa da corrente para cada degrau da escada,
  sem anotação manual.
- (Nota: sem narrativa de falha de rede/brown-out aqui — isso fica nas dificuldades do Cap. 4.)

## 3.5 Procedimento Experimental

**3.5.1 Checklist pré-ensaio — 1 parágrafo (itens em linha).** LiPo 2S ≥ 7,7 V em repouso
(cheia 8,4 V; abaixo do limiar, o corte de baixa tensão do ESC bloqueia o motor); bateria do
Raspberry carregada; notebook conectado à rede do Pi, ssh sem senha verificado.

**3.5.2 Protocolo do degrau — 2 parágrafos.**
- P1 (com força): tara da balança nos 3 s de neutro entre degraus (a corda relaxa 0,1–0,2 kg
  entre puxadas); após o comando, espera de 7 s (a resposta se assenta em ~4τ ≈ 7 s da
  dinâmica identificada — retomar no Cap. 4); força anotada nos segundos 7, 8 e 9; o ponto é
  a média das 3 leituras; mesmo protocolo na descida; sessão gravada em vídeo.
- P2 (aquisição contínua): mesmos degraus com o firmware rápido, registrando a corrente ao
  longo de todo o degrau (§3.4.2–3.4.3), sem anotação de força.

**3.5.3 Escadas — 1 parágrafo.** (a) Com força e vídeo: subida 97→117°, descida 117→97° —
faixa completa nos dois sentidos. (b) Aquisição contínua: subida 98→119°, descida 120→113°.
Degraus de 15 s; neutro de 3 s entre degraus.

**3.5.4 Ensaio em vazio — 1 parágrafo.** Rodas suspensas em caixa, sem contato com a mesa;
mesmos degraus; fornece I₀(u), a corrente sem carga usada na separação das perdas do modelo.

**3.5.5 Consolidação e validação — 1–2 parágrafos.** Os CSVs da aquisição contínua foram
consolidados por script dedicado, com regras objetivas por execução de degrau: pico acima de
60 A indica registro corrompido por falha de comunicação serial; degrau acima de 100° com
pico inferior a 3 A, ou a partir de 99° com pico inferior a 1 A, indica comando não executado;
duração inferior a 10 s, execução curta; o sentido da escada é inferido pelo arquivo de
origem. Das 58 execuções registradas, 54 foram validadas — subida 98–119° e descida 113–120°;
a ausência de descida abaixo de 113° na aquisição contínua é declarada como lacuna (a sessão
com força cobre 97–117° nos dois sentidos).

## 3.6 Incertezas de Medição — 3 parágrafos + TABELA

- P1 (Tipo A): dois níveis — dispersão das 3 leituras (7–9 s) dentro de cada ponto e
  dispersão entre as repetições da escada (repetibilidade do método); reportar os dois.
- P2 (Tipo B): balança — resolução 10 g, retangular, u = 5/√3 ≈ 2,9 g; leitura em vídeo —
  ±1 dígito quando houver dúvida de legibilidade; corrente — quantização de 122 mA, u ≈ 35 mA;
  relógio de quadros (±17 ms a 30 fps) — desprezível.
- P3 (sistemáticas e propagação): θ → cos θ = 0,995 (0,53%); r_ef < 0,5%; propagação em
  T = F·r_ef·cos θ por soma quadrática das componentes relativas. TABELA por faixa de degrau
  (gerar de `pfc kaka.xlsx` + consolidado).

## Resumo do Capítulo — 1 parágrafo
Ancoragem com geometria medida → cosseno quantificado → raio efetivo → cadeia de aquisição
verificada em bancada → degraus automatizados com registro em CSV → protocolo com vídeo e
tripla leitura → incertezas em dois níveis. Ponte ao Cap. 4.

---

## Ordem de escrita (um bloco por vez, autora valida cada)
1. 3.2 (cosseno) — números prontos;
2. 3.3 (roll-out) — pronto;
3. 3.4.1 P2 (verificação em bancada) — pronto;
4. 3.4.3 (ssh no laço + CSV) — pronto;
5. 3.1 (montagem) — precisa da foto;
6. 3.5 (procedimento) — pronto;
7. 3.4.1 P1+P3 + 3.4.2 (sensor e firmwares) — pronto;
8. 3.6 (incertezas) — eu gero a tabela antes;
9. Resumo.
