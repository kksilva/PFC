# Revisão Bibliográfica — Instrumentação, Monitoramento e Controle de Sistemas de Propulsão em Automodelos RC

Revisão executada em 26/10/2026 para fundamentar o Capítulo 2 (Seção 2.3) da monografia.
Fontes: BDTD/repositórios institucionais brasileiros, Google Scholar, periódicos (MDPI, Elsevier,
Springer, Cambridge) e relatórios técnicos oficiais (NASA NTRS, DTIC). Apenas trabalhos cuja
existência foi verificada em página/DOI/repositório. Chaves marcadas **[bib]** já constam em
`ListadeReferencias.bib`; as demais são candidatas a inclusão.

Legenda de relevância: ●●● diretamente relacionado · ●● correlato · ● contexto.

---

## 1. Trabalhos diretamente relacionados

### 1.1 Instrumentação e telemetria de veículos experimentais brasileiros

**[BR-1] Algoritmos de controle preditivo para seguimento de trajetórias de veículos autônomos**
Raffo, G. V. — UFSC (mestrado PPGEE), 2005.
Instrumentação embarcada do Mini-Baja UFSC (tacogerador de velocidade, ângulo de direção,
bússola) com submalhas de velocidade embarcadas em tempo real; validação experimental de
controladores preditivos (GPC).
https://repositorio.ufsc.br/bitstream/123456789/102008/1/223564.pdf — ●●●

**[BR-2] Desenvolvimento de um sistema eletrônico embarcado distribuído para telemetria veicular aplicado a veículos Baja SAE**
Silva, M. A. de L. (IFPB, Cajazeiras; orient. L. H. de Souza) — TCC Eng. de Controle e
Automação, 2026.
Três módulos ESP32 com CAN e LoRa; aquisição de RPM por sensores indutivos, temperaturas e
tensão de bateria; validação em bancada com indução de EMI junto a motor CC escovado; registro
em CSV.
https://repositorio.ifpb.edu.br/bitstream/177683/5149/1/TCC%20Miguel%20%C3%82ngelo%20de%20Lacerda%20Silva.pdf — ●●

**[BR-3] Acionamento vetorial de motores de indução trifásicos com enfraquecimento de campo e maximização do conjugado por ampère**
Gomes, L. C. — UFU (doutorado), 2008.
Capítulo dedicado a acondicionamento de sensores de corrente e tensão em DSP embarcado para
tração elétrica; bancada experimental de controle de velocidade.
https://repositorio.ufu.br/server/api/core/bitstreams/457d7542-2003-4ea6-a409-4294e78a5fe2/content — ●●

**[BR-4] Implementação de plataforma de coleta, armazenamento e visualização de dados para carro de competição**
Bernardo, G. C. et al. — UFSC, TCC, 2025.
Aquisição embarcada para prova de aceleração, com razão de escorregamento entre variáveis de
dinâmica veicular. Verificar conteúdo completo antes de citar (snippet confirmado).
https://repositorio.ufsc.br/bitstream/handle/123456789/267483/TCC.pdf?sequence=1 — ●●

### 1.2 Estimação de torque de BLDC por corrente

**[INT-1] Brushless DC Motor Electromagnetic Torque Estimation with Single-Phase Current Sensing**
Cham, C.-L.; Samad, Z. B. — Journal of Electrical Engineering and Technology 9(3), 2014.
Derivação e validação experimental da relação corrente–torque para back-EMF trapezoidal com
sensoriamento de fase única; conclui que a estimativa é válida em drives de baixa potência.
https://doi.org/10.5370/JEET.2014.9.3.866 — ●●●

**[INT-2] Load Torque Observer for BLDC Motors Based on a HOSM Differentiator**
Montero, C. et al. — Machines (MDPI) 11(12):1065, 2023.
Observador de torque de carga por correntes e posição, sem transdutor de torque, em
microcontrolador de baixo custo com FOC; convergência finita com rejeição de ruído.
https://www.mdpi.com/2075-1702/11/12/1065 — ●●●

**[INT-3] The Effect of Variable Torque Constant on Brushless DC Motor Torque Estimation**
Hung, C. W. et al. — ICIC Express Letters 12(8), 2018.
Quantifica a variabilidade da constante de torque K_t com corrente/posição e seu impacto na
estimativa; limites do método corrente→torque.
http://www.icicel.org/ell/contents/2018/8/el-12-08-09.pdf — ●●

**[INT-4] Modeling, Dynamic Characterization, and Performance Analysis of a 2.2 kW BLDC Motor Under Fixed Load Torque Levels**
Abouseda, A. I. et al. — Actuators (MDPI) 14(8):400, 2025.
Bancada com dinamômetro eletromecânico; confirma linearidade T × I em regime e desvios
crescentes com velocidade (perdas).
https://www.mdpi.com/2076-0825/14/8/400 — ●●

**[INT-5] Position and Speed Control of Brushless DC Motors Using Sensorless Techniques**
Gamazo-Real, J. C.; González-Sánchez, E.; Cárdenas, V. — Sensors 10(12), 2010.
Revisão clássica (400+ citações) das técnicas sensorless por back-EMF; fundamenta por que a
estimação interna do ESC é imprecisa em baixa rotação — a região do ensaio estático.
https://pmc.ncbi.nlm.nih.gov/articles/PMC3231115/ — ●●

### 1.3 Ensaio de tração (drawbar pull) — metodologia

**[bib: creager2017drawbar] Drawbar Pull (DP) Procedures for Off-Road Vehicle Testing**
Creager, C. — NASA/TM—2017-218924, 2017.
Formalização do ensaio de tração estático (força máxima com célula de carga) e dinâmico para
veículos off-road e robóticos; métricas DP, DP/peso, eficiência de tração.
https://ntrs.nasa.gov/api/citations/20170010706/downloads/20170010706.pdf — ●●●

**[INT-6] Mobility Performance Algorithms for Small Unmanned Ground Vehicles**
U.S. Army TARDEC — Relatório técnico DTIC ADA500849, ~2009.
Ensaios drawbar pull com célula de carga, rolo de corda e encoders; cálculo de escorregamento
e eficiência a partir de força, distância e velocidade.
https://apps.dtic.mil/sti/tr/pdf/ADA500849.pdf — ●●●

**[bib: abnt7899] ABNT NBR ISO 789-9:2020 — Ensaios de potência da barra de tração**
Adotada da ISO 789-9; aplicação brasileira discutida em Lanças, K. P., "Agricultural Tractor
Test", Rev. Ciências Agrárias (SciELO), 2020 [bib: lancas2020].
Ensaio estacionário de barra de tração com balança dinamométrica; condições de massa, engate e
incerteza replicáveis em escala reduzida — base normativa da adaptação ao automodelo.
https://www.scielo.br/j/rca/a/KLwhfzj5sLRBjJjW5chHqqC/?lang=en — ●●●

**[INT-7] Development of a Tow Capacity Test Device for Small Unmanned Ground Vehicles**
Barnett, R. — Virginia Tech (mestrado), ~2012.
Adaptação do procedimento militar TOP 2-2-604 de drawbar pull para UGVs pequenos, com célula
de carga e aquisição embarcada; dispositivo validado em campo.
https://vtechworks.lib.vt.edu/bitstream/handle/10919/30968/Barnett_Thesis.pdf — ●●●

**[INT-8] Parametric analysis of traction energy of an autonomous wheeled robotic system**
Shafaei, S. M. et al. — Research in Agricultural Engineering (Elsevier), 2023.
Ensaios instrumentados de força de tração × velocidade × consumo; 5,77–33,78 % da energia de
tração desperdiçada pelas rodas; tração mensurável com instrumentação simples.
https://www.sciencedirect.com/science/article/abs/pii/S0022489822000702 — ●●

### 1.4 Plataformas RC como veículo de pesquisa

**[bib: okelly2019f1tenth] F1TENTH: An Open-source Evaluation Environment for Continuous Control and RL**
O'Kelly, M. et al. (UPenn) — PMLR v123, 2020.
Chassi Traxxas Slash 1/10 + ESC VESC com telemetria de RPM; plataforma replicável por US$ 3–5
mil adotada por dezenas de universidades; odometria padrão baseada na telemetria do ESC.
https://proceedings.mlr.press/v123/o-kelly20a.html — ●●●

**[bib: goldfain2019autorally] AutoRally: An Open Platform for Aggressive Autonomous Driving**
Goldfain, B. et al. (Georgia Tech) — IEEE Control Systems Magazine 39(3), 2019.
RC trophy truck 1/5 com IMU, GNSS/RTK, encoders de roda e câmeras; documentação rigorosa da
cadeia de instrumentação; powertrain tratado como atuador não modelado.
https://arxiv.org/abs/1806.00678 — ●●

**[bib: evans2024f1tenth] Learning Dynamics Models for Velocity Estimation in Autonomous Racing**
Węgrzynowski, J. et al. — IROS 2024, pp. 972–979.
Mostra que encoder de roda sozinho falha em derrapagem; fusão com IMU/dinâmica necessária;
dataset público.
https://arxiv.org/abs/2408.15610 — ●●

**[INT-9] Autonomous Drift Cornering with Mixed Open-loop and Closed-loop Control (BARC)**
Gonzales, J. M. et al. (UC Berkeley) — IFAC 2017 / tese eScholarship.
Plataforma RC 1/10 de ~US$ 1 mil; identificação experimental de parâmetros dinâmicos (massa,
pneu) para controle em malha fechada de derrapagem.
https://escholarship.org/uc/item/3xb8f3d3 — ●●

**[INT-10] Advancing Autonomous Racing: A Comprehensive Survey of the RoboRacer (F1TENTH) Platform**
Equipe F1TENTH — arXiv:2506.15899, 2025.
Levantamento de 5 anos: confirma que o estado da arte trata ESC/motor como caixa-preta; nenhum
trabalho revisado caracteriza eletricamente o powertrain do automodelo.
https://arxiv.org/html/2506.15899v1 — ●●

### 1.5 Caracterização de motores de pequeno porte e medição de força de baixo custo

**[BR-5] Caracterização de motores Brushless de pequeno porte para veículos aéreos não tripulados**
Meyer, I. Z. L.; Barros, J. E. M. — Brazilian Journal of Development 7(6), 2021 (UFMG).
Bancada com sensor de torque e tacômetro; curvas torque × rotação × corrente × eficiência em
motores BLDC da classe hobby — mesmo porte do automodelo; trabalho da própria UFMG.
https://doi.org/10.34117/bjdv7n6-156 — ●●●

**[INT-11] A Low-Cost IoT-Based Bidirectional Torque Measurement System with Strain Gauge Technology**
Suciu, C. C. et al. — Applied Sciences (MDPI) 15(15):8158, 2025.
Torquímetro de strain gauge com HX711 (24 bits) e ESP8266; erro de poucos % em calibração —
valida o par strain gauge + HX711 proposto como continuação.
https://www.mdpi.com/2076-3417/15/15/8158 — ●●

**[INT-12] Design of Force Meter for Traction Unit**
(autores indonésios) — artigo em Neliti, ~2019.
Medidor de força de tração com ATmega328 + HX711 + célula tipo S; arquitetura idêntica à
proposta de continuidade do projeto.
https://media.neliti.com/media/publications/296552-design-of-force-meter-for-traction-unit-d3671ae7.pdf — ●●

**[INT-13] Terramechanics based wheel-terrain interaction model and its validation against field tests**
Jia, Z. et al. — Robotica (Cambridge), 2012.
Acoplamento canônico de medição de torque de acionamento e drawbar pull por faixa de
escorregamento sob carga conhecida — a relação T ↔ F que o projeto valida via T = f(I).
https://huei.engin.umich.edu/wp-content/uploads/sites/186/2015/02/Robotica_Jia-Terramechanics.pdf — ●●

## 2. Correlatos (contexto)

- **Malozyomov et al., 2024** — características de bateria de tração a partir de corrente/tensão
  embarcadas (World Electric Vehicle Journal 15(2):64). https://www.mdpi.com/2032-6653/15/2/64 — ●●
- **Mousavi, S. (Virginia Tech, 2021; IEEE 945995)** — raio efetivo de rolamento R_e = v/ω e
  patinamento por GPS; fundamenta a medida roll-out das rodas do automodelo.
  https://vtechworks.lib.vt.edu/bitstream/handle/10919/111783/Mousavi_H_D_2021.pdf — ●●
- **Implementação de Controle de Velocidade em Malha Fechada** — Instituto Mauá de Tecnologia
  (dissertação, repositório maua.br). Conteúdo não inspecionado; verificar antes de citar. — ●
- **Projeto Radio-Controlled Car (Mackenzie, 2018)** — projeto de disciplina no GitHub
  (zignd/mackenzie-projeto-rc-car); não é trabalho acadêmico formal. — ●

## 3. Lacunas na literatura (justificativa do projeto)

1. **Não existe caracterização torque × corrente validada de automodelo RC.** Em todas as
   plataformas revisadas (F1TENTH, AutoRally, BARC), o conjunto BLDC + ESC comercial é caixa-preta
   com mapeamento empírico PWM↔velocidade. Nenhum trabalho instrumenta o barramento com sensor
   de corrente de efeito Hall para caracterizar o powertrain.
2. **Não existe ensaio de tração estática (drawbar pull) em automodelos.** A metodologia é
   normatizada para tratores (NBR ISO 789-9) e adaptada a UGVs (NASA, TARDEC, Virginia Tech),
   mas nunca aplicada a chassis RC 1/8 de competição — a adaptação com balança de mola é inédita.
3. **Não existe validação cruzada corrente embarcada × força de tração medida em veículo RC.**
   A literatura ou mede F (ensaio de tração) ou estima T (drives BLDC em bancada); o cruzamento
   T = f(I) validado por balança em tração é a contribuição central do projeto.
4. **Efeito do raio efetivo de rolamento em pneus RC 1/8** não é coberto: a literatura de R_e
   trata de pneus automotivos; a deflexão de 6,1% medida no projeto não tem referencial.
5. **Caracterização da dinâmica do ESC modelístico** (rampa interna de corrente, τ ≈ 1,8 s
   dominado por soft-start/punch control) é ausente; os priors clássicos (L/R em ms) não se
   aplicam — resultado com consequência direta para controle.
6. **Literatura brasileira escassa**: produção nacional limita-se a telemetria de Baja SAE e
   instrumentação de Mini-Baja; nenhum TCC/dissertação brasileira sobre automodelo RC
   instrumentado foi localizada — reforça a originalidade.

## 4. Não verificados (não citar sem confirmar)

- Kelber et al. (2004) e Gomes (2003) — instrumentação do Mini-Baja UFSC, citados por Raffo (2005).
- TCC João Vitor Alvarenga Miotto (UFSC) — tração elétrica com sensor de corrente:
  https://repositorio.ufsc.br/bitstream/handle/123456789/248465/TCC__Joao_Vitor_Alvarenga_Miotto.pdf.pdf?sequence=3
- UTFPR PB_COELT_2021_1_01 (tração com frenagem regenerativa) — link 404 no repositório.
- Dissertação UTFPR PG_COELE_2017_2_19 (veículo autônomo "Cadu", UFMG) — não confirmada.
