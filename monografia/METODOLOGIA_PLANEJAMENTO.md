# Planejamento de Escrita — Capítulo 3 (Metodologia) — v3 detalhado

Fatos confirmados pela autora (26/10, noite):
- Cabo de 126 cm de cada lado da balança; balança a 15 cm do chão; engate a 28 cm do chão;
  medidas anotadas 3× → sen θ = 13/126 → θ = 5,9°; cos θ = 0,995 (correção ≤ 0,53%).
- Gancho engatado em estrutura traseira do veículo, ACIMA do eixo de transmissão.
- Tara nos 3 s de neutro entre degraus. Protocolo: espera 7 s após o comando; força anotada
  nos segundos 7, 8 e 9; ponto = média dos 3. Mesmo protocolo na descida. Tudo em vídeo.
- Massa total do conjunto: **6,640 kg** (anotado 3×). Efeito: μ do Cap. 4 = 0,80 (não 0,75).
- **Sensor: ACS758ECB-200B (±200 A)** a 3,3 V → 6,6 mV/A; offset 1,65 V; ADC 12 bits →
  122 mA/LSB (u_B quantização ≈ 35 mA).
- **O script de degraus (`teste_throttle.py`) foi disponibilizado pelo orientador** e executa
  DENTRO do Raspberry Pi, acionado por ssh a partir do notebook.
- Escadas: (a) com força + vídeo — subida 97→117°, descida 117→97°; (b) cego 100 Hz —
  subida 98→119°, descida 120→113° (rede caiu; 114° repetido por re-disparos).

---

## 3.1 Princípio do Ensaio de Tração Estática e Montagem

**P1 (abertura).** A caracterização exige duas grandezas simultâneas — força de tração e
corrente. A força só se manifesta em movimento; para medi-la em condição estacionária, o
veículo é ancorado: a reação da ancoragem iguala a tração, dispensando dinamômetro. Fechar com
a equação T_roda = F·r_ef (referencia §3.3).

**3.1.1 Configuração de ancoragem — 2 parágrafos.**
- P1: gancho da balança engatado na estrutura traseira do veículo, acima do eixo de
  transmissão; cabo de 126 cm em cada lado da balança; balança suspensa — 15 cm do chão do
  lado do padrão, 28 cm no engate do veículo; todas as dimensões anotadas 3×.
- P2 (liga ao 3.2): essa geometria define o ângulo do cabo, tratado na próxima seção.
- FIGURA: fotografia da montagem.

**3.1.2 Padrão de força e registro em vídeo — 2 parágrafos.**
- P1: balança digital de mala com gancho, resolução 10 g; alternativas rejeitadas
  (dinamômetro comercial — custo; célula de carga com registrador — proposta de continuidade,
  viabilizaria medição dinâmica).
- P2: a sessão inteira gravada em vídeo; cada ponto lido pausado, quadro a quadro, após o
  experimento — padroniza a leitura, elimina erro de pressa/paralaxe e dá rastreabilidade;
  justificativa: o display não tem saída elétrica.

**3.1.3 Massa adicional — 1 parágrafo.** Conjunto a 6,640 kg (massa adicional sobre o CG),
anotado 3×; função exclusivamente condicionante (carga normal → atrito disponível → patinagem
retardada); não entra no cálculo do torque; a condição de carregamento integra a especificação
do ensaio.

## 3.2 Geometria do Cabo e o Efeito Cosseno — 2 parágrafos

- P1: a balança mede a tensão no cabo; interessa a componente na linha de tração, F·cos θ;
  com as dimensões medidas (3×): sen θ = (28−15)/126 → θ = 5,9° → cos θ = 0,995 → correção
  máxima 0,53%, inferior à incerteza de leitura — θ desprezado por medida, não por hipótese.
- P2 (verificação independente): peso do veículo medido na vertical (5,140 kg, sem a massa
  adicional) e na horizontal com o cabo esticado concordam dentro de 0,2% — a montagem não
  introduz componente vertical mensurável.

## 3.3 Medida do Raio Efetivo da Roda — 1–2 parágrafos

Método roll-out: marcas no pneu e no solo; roda movimentada 5 vezes com o veículo encostado
na parede (direção de rolamento garantida reta); 3 anotações independentes; L = 236 cm →
r_ef = L/(2π·5) = 0,0751 m; nominal 80 mm (pneu novo, sem carga); deflexão de 6,1% sob carga;
usar r_ef em T = F·r_ef — usar o nominal injetaria 6% de erro sistemático.

## 3.4 Cadeia de Aquisição e Geração de Degraus

**3.4.1 Medição da corrente — 2 parágrafos.**
- P1: ACS758ECB-200B em série na alimentação; efeito Hall, isolado galvanicamente; alimentado
  a 3,3 V pelo Arduino Due; sensibilidade ratiométrica 6,6 mV/A a 3,3 V; saída 1,65 V em
  corrente zero; filtro RC ~24 Hz; ADC de 12 bits → resolução 122 mA/LSB.
- P2: dois firmwares — básico (100 amostras ADC consecutivas ~1 ms por ponto, 1 ponto/s;
  ensaio com forças) e rápido (período 10 ms, ~100 Hz; ensaio cego). Citar regras de
  amostragem (10–30× a banda) — reativar citações na rodada futura.

**3.4.2 Particularidade da aquisição a 100 Hz — 1 parágrafo.** O envio serial em rajadas faz
com que ~10 amostras cheguem com o mesmo timestamp (blocos de 100 ms); a ordem serial preserva
a sequência, de modo que o retempo válido é t = k×10 ms por índice; ~1550 amostras por bloco
de 15 s. Consequência: reconstrução do tempo, não perda de resolução.

**3.4.3 Geração dos degraus de comando — 3 parágrafos.**
- P1: o script de comando dos degraus foi disponibilizado pelo orientador e executa dentro do
  Raspberry Pi; o notebook o aciona remotamente por ssh
  (`ssh alunos@raspberrypi.local "python3 teste_throttle.py <ângulo> <duração>"`); o script
  coloca o ESC em neutro (95°), aplica o degrau pela duração programada e retorna ao neutro.
  Gerador de pulsos padrão servo (PCA9685): faixa 90–180°, comando normalizado u = (θ−95)/85.
- P2 (o problema): em degraus altos a rede entre notebook e Pi tornou-se o elo frágil —
  quedas do túnel ssh por brown-out do próprio Pi (bateria dedicada descarregada; step-down
  medido em 4,0 V contra 5,3 V esperados). Uma falha de rede é indistinguível de um comando
  não executado, e repetir degraus por rede corrompe a sequência.
- P3 (a solução — ensaio cego): script local que dispensa a confirmação de rede e ancora o
  protocolo na resposta elétrica: dispara o comando por ssh sem esperar retorno, abre a
  janela de aquisição no instante em que a corrente responde (limiar 0,3 A, acima do ruído de
  repouso de ±0,15 A; repouso abaixo de 0,5 A), re-dispara até 8 vezes por degrau (cobre o
  reboot do Pi de ~60 s) e garante o neutro ao final e em interrupção. A rede, quando viva,
  serve apenas para limpar processos órfãos antes de cada disparo. A validação do degrau
  deixa de depender do canal mais frágil e passa a usar o único canal confiável — a serial do
  sensor de corrente.

## 3.5 Procedimento Experimental

**3.5.1 Checklist pré-ensaio — 1 parágrafo (itens em linha).** LiPo 2S ≥ 7,7 V em repouso
(cheia 8,4 V; abaixo do limiar o LVC do ESC bloqueia o motor); bateria do Raspberry carregada
(episódio documentado: step-down em 4,0 V → resets e queda da rede); notebook conectado à
rede do Pi, ssh sem senha verificado.

**3.5.2 Protocolo do degrau — 2 parágrafos.**
- P1 (estático com força): tara da balança nos 3 s de neutro entre degraus (drift da corda de
  0,1–0,2 kg entre puxadas); após o comando, espera de 7 s (a resposta se assenta em ~4τ ≈ 7 s
  da dinâmica identificada — retomar no Cap. 4); força anotada nos segundos 7, 8 e 9; o ponto
  é a média das 3 leituras; idem na descida; sessão gravada em vídeo.
- P2 (dinâmico cego): mesma escala de degraus, aquisição a 100 Hz contínua no Due, janela
  ancora-se na resposta elétrica (§3.4.3); sem anotação de força.

**3.5.3 Escadas — 1 parágrafo + esquema.** (a) Com força + vídeo: subida 97→117°, descida
117→97° — faixa completa nos dois sentidos. (b) Cego: subida 98→119°, descida 120→113°,
interrompida pela queda da rede (o degrau 114° foi re-disparado até 5 vezes até obter janelas
válidas). Degraus de 15 s; tara/pausa de 3 s no neutro entre degraus.

**3.5.4 Ensaio em vazio — 1 parágrafo.** Rodas suspensas em caixa, sem contato com a mesa;
mesma escala de degraus; fornece I₀(u) — a corrente consumida sem torque na ponta, usada no
modelo de separação das perdas.

**3.5.5 Consolidação e validação — 1–2 parágrafos.** Script consolidador sobre os CSVs cegos
(corrente ao longo do tempo); regras objetivas: pico > 60 A = registro corrompido (falha
serial); degrau > 100° com pico < 3 A, ou ≥ 99° com pico < 1 A = comando não executado;
duração < 10 s = execução curta; sentido da escada inferido pelo arquivo de origem (correção
de rotulagem). Resultado: 58 registradas → 54 validadas; cobertura subida 98–119°, descida
113–120°; lacuna: descida 98–112° (somente da sessão cego).

## 3.6 Incertezas de Medição — 3 parágrafos + TABELA

- P1 (Tipo A): dois níveis — dispersão das 3 leituras (7–9 s) dentro de cada ponto (flutuação
  de curta duração + leitura) e dispersão entre as repetições da escada (repetibilidade do
  método); reportar os dois.
- P2 (Tipo B): balança — resolução 10 g → retangular, u = 5/√3 ≈ 2,9 g; leitura em vídeo —
  ±1 dígito quando houver dúvida de legibilidade (condição de filmagem); corrente — quantização
  122 mA → u ≈ 35 mA; resolução do relógio de quadros (±17 ms a 30 fps) — desprezível na
  janela.
- P3 (sistemáticas pequenas e propagação): θ → cos θ = 0,995 (0,53%); r_ef < 0,5%; propagação
  em T = F·r_ef·cos θ por soma quadrática das componentes relativas. TABELA por faixa de
  degrau (gerar de `pfc kaka.xlsx` + consolidado).

## Resumo do Capítulo — 1 parágrafo
Montagem ancorada com geometria medida → cosseno quantificado → raio efetivo → cadeia de
aquisição com dois firmwares → geração de degraus com validação elétrica → protocolo com
vídeo e tripla leitura → incertezas em dois níveis. Ponte ao Cap. 4.

---

## Ordem de escrita (um bloco por vez, autora valida cada)
1. 3.2 (cosseno) — números todos prontos;
2. 3.3 (roll-out) — pronto;
3. 3.4.3 (degraus: orientador → rede → cego) — pronto;
4. 3.1 (montagem) — precisa da foto;
5. 3.5 (procedimento) — pronto;
6. 3.4.1 + 3.4.2 (corrente + rajadas) — pronto;
7. 3.6 (incertezas) — eu gero a tabela antes;
8. Resumo.
