# Itens a verificar no texto da monografia

Checklist de afirmações/valores que precisam ser conferidos contra a fonte primária (dados de
ensaio, datasheet, medição própria) antes da entrega. Marcar `[x]` quando confirmado, anotando
a fonte/valor correto.

- [ ] **1. Valor de redução do motor** — `DescricaoProcesso.tex`, Seção 2.1: texto afirma
  "redução mecânica total estimada em $i \approx 11{,}5$". Confirmar: (a) se o valor é 11,5
  mesmo; (b) como foi obtido (medição própria, cálculo a partir da relação de dentes
  pinhão/coroa, ou valor do orientador — conforme nota em `PLANEJAMENTO_MONOGRAFIA.md`); (c)
  se cabe citar a fonte explicitamente no texto.

- [x] **2. Taxa de descarga máxima da bateria (C-rate)** — Confirmado: 60C. Corrente
  contínua máxima ≈ 312 A (60 × 5,2 Ah), acima do limite de 120 A do ESC — portanto o ESC é
  o fator limitante, não a bateria. Já incluído em `DescricaoProcesso.tex`, Seção 2.1.

- [x] **3. Fonte da Figura "motor_brushless.png"** — Confirmado: Gator Lamination,
  <https://www.gatorlamination.com/bldc-motor-stator-and-rotor/> (site de fabricante
  chinês, sem data de publicação, copyright 2026). Citada em `ListadeReferencias.bib`
  (`gatorlamination2026`) e na legenda da Figura~2.1 de `DescricaoProcesso.tex`.
  **Pendência separada:** a imagem é de um site comercial de terceiro, sem licença
  explícita de uso — avaliar se é necessário pedir permissão antes da entrega final, ou
  substituir por um diagrama próprio (TikZ), já que a legenda trata o desenho como
  genérico (não mostra a topologia inrunner específica do motor do automodelo).

## Registro do problema de degraus sobrepostos (ensaio)

- [x] **4. Causa do defeito "degrau sobrepor o outro"** — Dois gatilhos identificados:
  (a) **LVC da bateria gasta/estufada**: sob carga a tensão caía, o ESC reduzia o próprio
  duty internamente para se proteger → comando de degrau alto executado com força/corrente
  de degrau menor (ex.: 110° lido como 102°). Não era sobreposição de código;
  (b) **dessincronização notebook↔Raspberry**: o comando era lançado com `subprocess.Popen`
  (sem esperar o término) e o próximo degrau podia iniciar antes do Pi retornar ao neutro,
  rotulando leituras do degrau anterior com o ângulo errado.
  **Correção aplicada** (commits `b115264` e `8e06ec5`, scripts `~/PFC/ensaios/`):
  `proc.wait(timeout=20)` + `time.sleep(3)` de folga garantem que o Pi terminou antes do
  próximo degrau; print da corrente a cada segundo permite detectar "encolhimento" de
  degrau em tempo real. **Condição para não recorrer:** bateria LiPo 2S saudável e
  carregada (a gasta foi descartada).
  Fonte desta análise: conversa 21–22/10/2026, seção 4.4 do plano (fontes de erro).

## Checklist do ensaio definitivo (bateria nova)

- [ ] Renomear `NOME_CSV` para arquivo novo (`subida_bateria_nova_1.csv` etc.) — CSVs
  antigos têm 4 colunas e não combinam com o novo formato (5 colunas + série/marcador)
- [ ] Ajustar `ANGULO_INICIAL`/`ANGULO_FINAL`: subida 95→~125°, descida 125→95°
  (força não saturou em 115°; platô esperado ~120–125°)
- [ ] **Bateria LiPo 2S: MEDIR a tensão em repouso antes de cada série** —
  <= 7,0 V (2S) = descarregada: o LVC do ESC bloqueia o motor e o sintoma
  e' indistinguível de falha de rede/throttle (pico < 0,3 A, 'sem resposta'
  em todos os degraus — episodio 24/10 ~15:44). Cheia = 8,4 V, meia carga
  ~7,7-7,8 V. Recarregar em modo balance (2S). (Antigo item: verificar tensão por célula antes
- [ ] Halteres 1 kg ×2 fixados sobre o CG (fita/velcro), massa total anotada (~7,1 kg)
- [ ] **Tara da balança a cada degrau** — registrar a leitura de repouso (ex.:
  0,202 kg) ANTES de tarar, depois zerar e anotar a força. O conjunto
  corda/suspensão relaxa a cada puxada (drift tipo passeio aleatório, ~0,1–0,2
  kg entre degraus); tarar a cada degrau elimina o erro acumulado na força
  (decisão 24/10, rigor). Nunca tarar durante o degrau.
- [x] θ: DESPREZÍVEL por decisão (balança suspensa pela alça alinha o eixo à linha de tração; θ residual só da geometria de engate) — ver `PLANEJAMENTO_MONOGRAFIA.md` §3.3, marcado RESOLVIDO em 22/10/2026
- [ ] **Notebook na rede do Raspberry — verificar ANTES de cada série** —
  comando `iwgetid -r` deve retornar o SSID do Pi (se retornar outra rede, ex.:
  "UFMG", o notebook saltou de rede e o ssh falha com "could not resolve
  hostname", imitando uma queda do Pi — episódio de 24/10, descida). Confirmar
  também com `ssh alunos@raspberrypi.local` sem senha. Se o soquete ssh estiver
  velho: `rm -f /tmp/pfc-ssh.sock`.
- [ ] ≥3 séries (subida + descida) para repetibilidade/histerese
- [ ] Anotar força da balança nos últimos 3 s de cada degrau (janela 7–10 s)

## Registro do problema de rede caindo em degraus altos (ensaio 24/10)

- [ ] **5. Causa das quedas do túnel ssh / Pi inalcançável em degraus 105–107** —
  Sintomas: `Connection to 10.42.0.1 port 22 timed out`, soquete mestre quebrado,
  "sem confirmacao" em 3 tentativas, com o carro rodando. Hipótese inicial: EMI/queda
  de tensão no pico de corrente (bateria LiPo nova entregando mais corrente). **Causa
  principal descoberta posteriormente: a bateria dedicada do Raspberry Pi estava
  descarregada** — o Pi sofria brown-out e a rede (WiFi e Ethernet) sumia até ele voltar
  (ou não voltava). A correlação com degraus altos foi coincidência acumulada, não
  causa. **Evidência elétrica (24/10):** tensão medida na saída do *step-down* do Pi
  caiu para **4,0 V** (valor esperado ≈ **5,3 V**) — abaixo do mínimo operacional do
  Raspberry Pi (~4,75 V), condição suficiente para os resets e a queda da rede.
  **Para o relatório (Cap. 3 Metodologia / Cap. 4 Dificuldades):** registrar como
  fonte de falha da telemetria — autonomia da bateria do computador de bordo; medida
  corretiva: verificar/caregar a bateria do Pi no checklist pré-ensaio + script `rodar_
  ensaio_cego.py` (dispara sem rede e ancora a janela na resposta elétrica da corrente).
  **Condição para confirmar a causa:** refazer um degrau alto com a bateria do Pi
  carregada e observar o link permanecer estável (latência reportada pelo script).
  Fonte: logs do ensaio de 24/10/2026 (conversa, seção "auditoria do túnel").

- [ ] **6. Cadeia de aquisição: relatos vs. firmware real** — Os relatórios
  descrevem três cadeias diferentes: Parcial 2 (média de 500 amostras com 2 ms
  de intervalo = integração de ~1 s); Relatório Experimental (filtro RC de
  ~24 Hz + média móvel digital de 200 amostras em 100 ms, Nyquist citado em
  1 kHz); firmware efetivamente gravado no Due (`Sensor_de_Corrente_ACS758.ino`:
  100 leituras ADC consecutivas ~1 ms + `delay(1000)` = 1 ponto/s). **Cap. 3 deve
  documentar a cadeia as-built** (100 amostras/ponto, 1 Hz, filtro RC 24 Hz) e
  o Cap. 4 deve declarar como limitação a subamostragem do regime de patinagem
  cíclica (ciclos ~2 s > Nyquist de 0,5 Hz) — com proposta de continuidade
  (aquisição a maior taxa para caracterizar o stick-slip).

## Decisao de taxa de amostragem (auditoria 24/10)

- [ ] **7. Duas taxas, dois objetivos** — O dado a 1 Hz (ensaio de escada) serve
  para a curva estatica torque x corrente e para o envelope da patinagem, mas NAO
  para identificacao de função de transferencia: o stick-slip (~2 s de periodo)
  fica no limiar de Nyquist (0,5 Hz) e a resposta de corrente do ESC (~10-100 ms)
  e invisivel. Para a dinamica, protocolo dedicado a ~100 Hz (20 amostras ADC por
  ponto, `Sensor_de_Corrente_ACS758_fast`, delay 5 ms), pulsos de 1-2 s entre
  100-110° (regime de aderencia; TF e linear), neutro de 1 s entre pulsos, >=5
  pulsos com amplitudes variadas. Regras de decisao: 10-30x a banda
  (Åström & Wittenmark 1997; Franklin 1998) e 10-20 amostras no tempo de subida
  (Clarke 1984 em Ljung 1999): banda de interesse ~5-10 Hz (ciclos de patinagem +
  transientes de corrente) -> fs ~100 Hz; o filtro RC de 24 Hz assume o papel de
  anti-aliasing (fc ~ Nyquist/2). **Limitacoes a declarar no Cap. 4:** (a) forca
  da balanca so existe a 1 valor/degrau (display) — a dinamica u->F exigiria celula
  de carga com registrador (proposta de continuidade: HX711, ~R$30); (b) com o
  veiculo ancorado identifica-se o subsistema ESC+motor+tração, nao a dinamica
  longitudinal do veiculo (que exige velocidade — IMU/encoder das alternativas do
  Cap. 2). Citar \cite{ljung1999system, astrom1997computer, franklin1998digital}.
- [ ] **8. Pipeline identificacao -> controlador (Cap. 4/5)** —
  (1) curva estatica T x I/u (escada 1 Hz — CONCLUIDA 24/10, ensaio_cego_subida.csv);
  (2) G1(s)=I/u em bancada ancorada a 100 Hz (firmware fast, pulsos 1-2 s,
  100-110°); (3) G2(s)=v/u com carro livre, pulsos 100-110°, velocidade por
  IMU/encoder (secao 2.2.1) — ou fallback: malha fechada de CORRENTE/torque na
  bancada (Pi + PI + ACS758), que demonstra PSR sem medicao de velocidade;
  (4) ajuste FOPDT (Ljung 1999), PI com ganho programado pela curva estatica,
  anti-windup e rate-limit da referencia (ligar com a "protecao" da sec. 2.2.1);
  validar PSR/PRP em simulacao e, se possivel, malha fechada real com o Pi.

## VALORES FECHADOS para o modelo teorico (24/10, pos-auditoria)

Normalizacao do comando: u = (angulo - 95)/85, u em [0,1] (95 = neutro, 180 = max;
1 unidade = faixa inteira do ESC, coerente com o PWM 1-2 ms da sec. 2.2.1).

- Regiao de identificacao: angulo 100-110 graus. Embasamento: regressao linear da
  fase de aderencia sobre ensaio_cego_subida.csv da I(angulo): r2 = 0,970, residuos
  <= +-/10% (tipico 3-5%). Abaixo de 100: curvatura de partida (transiente de
  engate); de 110 em diante: stick-slip (nao-linear, fora do modelo linear).
- Ponto nominal: angulo0 = 105 graus (centro da faixa), u0 = 0,118, I0 = 12,2 A
  (medido). Modelo em desvios: I_til = I - 12,2; u_til = u - 0,118.
- Ganho estatico: K = 120 A/u (= 1,42 A/grau, regressao 100-110). Confirmar com o
  ensaio dinamico (pulsos).
- Dinamica (PENDENTE - ensaio 100 Hz): FOPDT G1(s) = K exp(-theta_a s)/(tau s + 1);
  priors a confirmar: theta_a em [0,02; 0,1] s, tau em [0,05; 0,3] s (resposta
  tipica de ESC + constante eletrica L/R). Protocolo: pulsos de 2 s, neutro 1 s,
  amplitudes {100,102,104,105,106,108,110} em ordem embaralhada, >= 3 repeticoes;
  2 s = 6-40 tau (garante regime); 100 Hz = 14x a banda do transitorio mais rapido
  (subida ~50 ms -> 7 Hz), atende 10-30x (Astrom/Franklin).
  PROTOCOLO REVISADO (24/10, pos-questionamento da autora): em vez de pulsos
  separados, REFAZER A ESCADA 100-110 com os MESMOS degraus de 15 s, so que a
  100 Hz: cada borda de subida e uma resposta ao degrau (identifica zona morta +
  FOPDT, estrutura Hammerstein) e cada plato (media dos ultimos 5 s) e o ponto
  estatico com a forca da balanca. ACRESCENTAR pulsos curtos de +/-2-3 graus em
  torno de 105 (ex.: 105->108->105, 105->102->105, >= 3 repeticoes, 1-2 s) para o
  modelo LINEAR em desvios usado no projeto do PI. Racionalidade: ponto fixo
  precisa de >= 5-10 tau (0,5-3 s); alem de ~10 tau a duracao extra nao agrega
  dinamica, so repeticoes agregam estatistica; K pode vir da curva estatica se o
  pulso for mais curto que o assentamento.
- Nao linearidades (do proprio dado estatico): zona morta u <= ~0,03 (angulo <= 97,
  I ~ 0); saturacao de aderencia a partir de angulo ~110 -> u_sat ~ 0,18; T_max =
  F_max * r (F_max = maior forca anotada nos picos de 115-116; I associada 29-33 A).
- Rendimento: eta = F*r/(i*Kt*I) ponto a ponto (Kt = 4,55 mN m/A do 2100 KV,
  i = 11,5) — fecha a validacao teorica; esperado 0,8-0,9.
- Controlador (teorico, simulacao): PI-IMC com Kp = tau/(K(lambda+theta_a)),
  Ti = tau, lambda = 0,2 s (=> ts ~ 0,6 s; coerente com a protecao da transmissao,
  sec. 2.2.1); Ts = 10 ms; anti-windup por clamp + rate-limit |du/dt| <= 1 u/s.
- Validacao em simulacao: PSR (degrau): Mp <= 10 %, ts ~ 0,6 s, ess = 0;
  PRP (degrau de perturbacao +20 % na planta, t = 5 s): desvio max e recuperacao;
  robustez: GM >= 6 dB, PM >= 30 graus com K +-/20 %, tau +-/30 %.
- Suficiencia da curva plotada: estatica SIM (depende das forcas anotadas 98-117:
  da ganhos, zona morta, saturacao e eta); dinamica NAO — falta apenas o ensaio de
  pulsos a 100 Hz (firmware ja compilado; ~1 tarde).
- [ ] **9. Raio efetivo da roda (r em T = F*r)** — Nominal (fabricante, pneu
  novo sem carga): diametro 160 mm -> r_nom = 80 mm (pag. oficial Kyosho 30888,
  "Tire(F/R) 160 x 100 mm"). Usar o RAIO EFETIVO (de rolamento), menor que o
  geometrico por deformacao do pneu sob carga (tip. 2-5 %): medir por roll-out —
  marcar pneu e chao, rolar o carro em linha reta SEM patinar por 10 voltas,
  medir L, r_ef = L/(10*2*pi), 3 repeticoes, com os halteres (mesma carga normal
  do ensaio). Reportar os tres valores (nominal, carregado, efetivo) no Cap. 3;
  incerteza do roll-out < 0,5 %.
- [ ] **10. Ensaio em vazio com SS41F** — Registrar no relatorio (Cap. 3
  metodologia/limitacoes ou Cap. 5 propostas) que o sensor magnetico SS41F
  (alternativa ja discutida na sec. 2.2.2) viabilizaria o ENSAIO EM VAZIO:
  anel magnetizado no eixo/roda + SS41F mediriam a rotacao com o veiculo
  suspenso/ancorado-sem-carga, permitindo medir Kv real do motor
  (n = Kv * E), a corrente de vazio I0, a curva rpm x throttle e a dinamica
  u -> omega (identificacao do motor livre, sem carga de tracao). PESQUISAR
  DEPOIS: metodologia de medicao de Kv com ESC no caminho (estimativa da
  tensao efetiva via razao ciclica), incertezas, e o que a dinamica u->omega
  em vazio agregaria ao modelo (comparacao com a dinamica sob carga, estimativa
  de J e B da Eq. dinamica rotacional).
- [x] **11. Consolidacao dos dados de ensaio (24/10)** — `ensaios/consolidar_
  dados.py` gera `ensaio_consolidado.csv`: 58 execucoes VALIDADAS (subida
  98-120 com 1-2 repeticoes; descida 113-120 com 114 5x; histerese completa
  na faixa alta). Regras: pico>60 A = CORROMPIDO (era serial 115200);
  degrau>100 com pico<3 A ou degrau>=99 com pico<1 A = SINAL_FRACO; dur<10 s
  = CURTO. **Cap 4 deve usar apenas o consolidado.** Lacunas declaradas:
  descida 101-112, dinamica (FOPDT por priors + robustez ate nova sessao).
