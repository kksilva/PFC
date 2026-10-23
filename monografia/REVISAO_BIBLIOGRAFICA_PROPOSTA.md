# Revisão bibliográfica — fontes levantadas para a monografia

Lista de todas as fontes que localizei e verifiquei ao longo do projeto (algumas já estavam
em `ListadeReferencias.bib`, outras foram adicionadas em sessões de pesquisa mais recentes).
O `.bib` foi esvaziado e todas as citações (`\cite{}`) foram removidas do texto a seu pedido —
esta lista serve para você decidir quais recolocar, e onde. Para cada fonte: resumo do
conteúdo, por que eu queria usá-la, e em que trecho do texto ela se encaixaria.

Observação sobre confiabilidade: a maioria foi verificada diretamente (datasheet, manual,
PDF da tese/artigo, página do fabricante). Duas exceções estão marcadas abaixo como "não
verificado diretamente" — a informação vem de busca na web, sem acesso ao documento original.

---

## Especificações de componentes (datasheets e manuais de fabricante)

### `kyosho` — Kyosho Corporation, *Mad Force Kruiser VE Readyset: Instruction Manual*
- **Resumo:** manual do fabricante do automodelo. Contém as especificações do ESC Orion
  Vortex R8 (corrente contínua 120 A, pico 760 A) e dados gerais do kit.
- **Motivo:** é a fonte primária dos números de corrente do ESC citados na Seção 2.1.
- **Como usar:** citar junto à frase "o controlador suporta corrente contínua de até 120 A e
  corrente de pico de até 760 A" (Seção 2.1, após o parágrafo da comutação).

### `allegro` — Allegro MicroSystems, *ACS758 datasheet* (Rev. 4, 2022/2024)
- **Resumo:** datasheet oficial do ACS758. Confirmei por extração direta do PDF: tempo de
  subida (rise time) 3 µs, tempo de resposta total 4 µs, largura de banda interna 120 kHz.
- **Motivo:** fonte primária dos números usados para justificar que o ACS758 tem banda
  suficiente frente ao chaveamento do ESC (Seção 2.2.4).
- **Como usar:** citar junto aos números "3 µs", "4 µs" e "120 kHz" no parágrafo do ACS758.

### `ti_ina240_2` — Texas Instruments, *INA240: Bidirectional Current-Sense Amplifier with
  Enhanced PWM Rejection* (página de produto, ti.com)
- **Resumo:** página de produto do INA240, com o dado de largura de banda de 400 kHz e os
  ganhos fixos disponíveis (20/50/100/200 V/V).
- **Motivo:** fonte do número "400 kHz" usado para justificar a margem de banda do INA240
  frente ao chaveamento do ESC (Seção 2.2.3).
- **Como usar:** citar junto à frase "largura de banda de 400 kHz e rejeição reforçada a
  transientes de modo comum".

### `ti_ina240` — Texas Instruments, *INA240 Current-Sense Amplifiers* (datasheet genérico)
- **Resumo:** versão mais antiga/genérica do datasheet do INA240, sem o dado específico de
  banda que está em `ti_ina240_2`.
- **Motivo:** foi a primeira referência ao INA240 que eu tinha, antes de localizar a página de
  produto com o dado de 400 kHz. Hoje é redundante.
- **Como usar:** provavelmente descartável em favor de `ti_ina240_2`; mantenha só se quiser
  citar o datasheet completo (pinagem, diagrama) em vez da página de produto.

### `invensense_mpu` — InvenSense, *MPU-6050 Six-Axis MEMS MotionTracking Device* (datasheet)
- **Resumo:** datasheet oficial do sensor IMU MPU6050.
- **Motivo:** fonte das especificações do sensor citado como exemplo na Seção 2.2.1 (IMU).
- **Como usar:** citar junto à primeira menção ao "MPU6050" na Seção 2.2.1.

### `honeywell_ss41f` — Honeywell, *SS41F/SS41G: Low-Cost Digital Bipolar Hall-Effect Sensor
  ICs* (2015)
- **Resumo:** datasheet do sensor Hall digital SS41F/SS41G (sensor bipolar, saída digital).
- **Motivo:** fonte primária das especificações citadas na Seção 2.2.2.
- **Como usar:** citar na primeira menção ao sensor, no início da Seção 2.2.2.

### `yge_esc` — YGE, *Brushless Electronic Speed Controllers: Operating Instructions*
  (manual do fabricante)
- **Resumo:** manual de um ESC brushless genérico (não é o da Kyosho/Orion), confirma faixa
  de chaveamento PWM de 8 a 16 kHz, ajustável em passos de 1 kHz.
- **Motivo:** é a fonte do número "8 kHz a 16 kHz" usado repetidamente para comparar a banda
  dos sensores de corrente (INA240 e ACS758) com a frequência de chaveamento típica de um ESC
  sensorless. É um ESC diferente do da Kyosho — usei por analogia, já que o manual da Kyosho
  não divulga a frequência de chaveamento do Orion Vortex R8.
- **Como usar:** citar nas Seções 2.2.3 e 2.2.4, junto às menções à faixa "8 kHz a 16 kHz".
  Vale deixar claro no texto que é um valor típico de ESCs sensorless dessa classe, não o
  valor medido do Orion Vortex R8 especificamente.

### `arduino_due` — Arduino, *Arduino Due: Product Reference Manual*
- **Resumo:** manual técnico oficial do microcontrolador Arduino Due.
- **Motivo:** fonte primária das especificações do microcontrolador usado na aquisição dos
  sinais (ADC, clock, etc.) — relevante para o Capítulo 3 (Metodologia), ainda não escrito.
- **Como usar:** citar na Metodologia, ao descrever o hardware de aquisição.

### `gatorlamination2026` — Gator Lamination, *BLDC Motor Stator and Rotor* (site do
  fabricante)
- **Resumo:** site comercial chinês com uma imagem genérica de estator/rotor de motor BLDC,
  usada hoje como Figura 2.1. Sem data de publicação, copyright genérico do site.
- **Motivo:** foi a única imagem didática que encontrei do princípio de funcionamento de um
  motor brushless. Não tem licença explícita de uso.
- **Como usar:** **pendência em aberto** (ver `TODO_VERIFICAR.md`, item 3) — decidir entre
  manter com essa citação (site comercial, sem licença clara), pedir permissão ao site, ou
  substituir por um diagrama próprio em TikZ, o que resolveria o problema de licença de uma
  vez.

---

## Artigos e trabalhos acadêmicos

### `monteiro2016` — Monteiro, *Medição indireta de torque e velocidade angular de motor de
  corrente contínua sem escovas* (dissertação, UFSC, 2016)
- **Resumo:** dissertação de mestrado da UFSC sobre medição indireta de torque e velocidade
  angular de um motor BLDC — tema muito próximo ao deste projeto.
- **Motivo:** é o precedente acadêmico brasileiro mais direto que encontrei para a abordagem
  de estimação indireta de torque. Ainda não citado no texto atual.
- **Como usar:** citar na Seção 2.2, como precedente nacional da abordagem de medição indireta
  de torque via corrente — encaixaria bem na introdução reescrita da seção ou na Síntese
  Comparativa.

### `bomfim2021` — Bomfim, *Controle, Telemetria e Instrumentação de um Automodelo*
  (Projeto de Graduação, UnB, 2021)
- **Resumo:** TCC da UnB que instrumentou e controlou um automodelo off-road 1:10 com sensores
  inerciais, magnetômetro e odômetro óptico para estimar a trajetória. Não mede grandezas
  elétricas do sistema de propulsão.
- **Motivo:** precedente acadêmico brasileiro direto de instrumentação de automodelo — usei
  para evidenciar a lacuna (não medir corrente/torque) que este trabalho preenche.
- **Como usar:** citar na introdução da Seção 2.2 (Estado da Arte), como exemplo de
  instrumentação de automodelo em âmbito nacional que não aborda grandezas elétricas.

### `nakashima2021` — Nakashima, *Análise do motor CC sem escovas* (UNESP, 2021)
- **Resumo:** trabalho acadêmico brasileiro (UNESP) sobre análise de funcionamento de motores
  BLDC.
- **Motivo:** precedente nacional para a explicação de funcionamento do motor brushless e da
  comutação eletrônica.
- **Como usar:** citar na Seção 2.1, ao explicar o princípio de funcionamento do motor
  brushless e da comutação eletrônica.

### `borges2016` — Borges, Sobrinho, Lima Filho e Belo, *Métodos e técnicas de medição de
  torque diretamente em eixos rotativos* (Revista Principia/IFPB, 2016)
- **Resumo:** artigo de revisão brasileiro sobre métodos de medição direta de torque em eixos
  girantes (células de carga, extensômetros, etc.).
- **Motivo:** dá base de revisão nacional sobre métodos de medição de torque, útil para
  contrastar com o método indireto (via corrente) escolhido neste trabalho.
- **Como usar:** citar na Metodologia (Capítulo 3), ao justificar a escolha do método indireto
  frente aos métodos diretos tradicionais revisados no artigo.

### `sharma2019` — Sharma, Pal, Mahalle, Botre e Akbar, *The Development of Current, Speed
  and Torque Measurement System for Low Power Electric Vehicle Motion Control Applications*
  (ETMN, 2019)
- **Resumo:** usa um sensor de efeito Hall em um motor brushless tipo hub, relacionando a
  corrente de fase medida à força de tração, à potência e à eficiência de um veículo elétrico
  de baixa potência.
- **Motivo:** é o precedente mais direto que encontrei da abordagem considerada neste
  trabalho (corrente de fase → torque/tração em veículo elétrico pequeno).
- **Como usar:** citar na Seção 2.2.4 (ACS758/ACS712), junto à frase sobre "precedente direto
  da abordagem considerada neste trabalho".

### `dumitrascu2020` — Dumitrascu, Bordea e Cazan, *On the Improvement of Performance in
  Motorsport by Means of Acceleration Measurements* (SPIE, 2020)
- **Resumo:** usa um MPU6050 para monitorar a atitude de um veículo de duas rodas ao longo de
  uma pista.
- **Motivo:** exemplo de uso de IMU em veículo de pequeno porte, ilustrando a viabilidade da
  técnica na Seção 2.2.1.
- **Como usar:** citar na Seção 2.2.1 (IMU), junto ao exemplo do MPU6050.

### `meisner2021` — Meisner, *Practical Comparison of Different Current Measurement
  Technologies for Use in Variable Frequency Drives* (dissertação, Tampere University, 2021)
- **Resumo:** comparação prática entre shunt resistivo e sensores de efeito Hall para medição
  de corrente em acionamentos de frequência variável; conclui que o shunt tem bom desempenho
  estático, mas desempenho dinâmico inferior ao Hall sob chaveamento rápido.
- **Motivo:** é a fonte central que usei para justificar a preferência pelo ACS758 (Hall)
  sobre o shunt+INA240, com base em desempenho dinâmico.
- **Como usar:** citar nas Seções 2.2.3 (INA240) e 2.2.4 (ACS758), junto às duas afirmações
  sobre desempenho dinâmico inferior do shunt.
- **Atenção:** não consegui acessar o PDF completo diretamente — o repositório da Tampere
  University (trepo.tuni.fi) bloqueou o download (proteção anti-bot). A informação acima vem
  de resumos/buscas na web, não de leitura direta do texto. Vale confirmar o conteúdo exato
  antes de citar, se possível acessando a tese por outro caminho.

### `theys2021` — Theys e De Schutter, *Virtual Motor Torque Sensing for Multirotor Propulsion
  Systems* (IEEE Robotics and Automation Letters, 2021)
- **Resumo:** método que estima o torque de um motor brushless de multirrotor a partir apenas
  da tensão de alimentação, do comando de aceleração e da velocidade de rotação, ajustando um
  modelo de quatro parâmetros ao conjunto motor-ESC-hélice — sem usar sensor de corrente.
- **Motivo:** é um contraponto importante: mostra que existe uma alternativa sem sensor de
  corrente, o que usei para justificar por que a medição direta de corrente é preferível no
  seu projeto (é mais geral, não exige recalibração por motor/ESC/carga).
- **Como usar:** citar na Síntese Comparativa (2.2.5), como "terceira via" alternativa à
  medição de corrente.
- **Nota:** confirmado por referência cruzada (portal de pesquisa da KU Leuven + registro
  Unpaywall do DOI 10.1109/LRA.2021.3068068), não pela leitura direta do PDF (o link direto
  retornou erro 404).

### `liu_kriging` — Liu, Li, Ma e Xu, *Kriging Assisted On-line Torque Calculation for
  Brushless DC Motors Used in Electric Vehicles* (relatório técnico, University of
  Michigan–Shanghai Jiao Tong University Joint Institute)
- **Resumo:** nota que a relação entre corrente e torque de um motor BLDC deixa de ser
  aproximadamente linear em correntes elevadas.
- **Motivo:** fonte da ressalva sobre não linearidade em correntes altas, usada para justificar
  a necessidade de calibração experimental no Capítulo 3.
- **Como usar:** citar na Seção 2.2.4 (ACS758/ACS712), junto à ressalva sobre não linearidade
  em correntes elevadas.
- **Atenção:** o download direto do PDF falhou (retornou uma página de erro HTML, não o PDF).
  Ano de publicação não confirmado (está como `n.d.` no `.bib` original). Vale tentar
  encontrar uma versão publicada/com ano antes de citar.

### `motioncontroltips_kt` — Motion Control Tips, *FAQ: What Is the Difference Between Torque
  Constant, Back-EMF Constant, and Motor Constant?* (site técnico)
- **Resumo:** artigo técnico que explica a relação $K_t \approx 9{,}55/K_v$ entre a constante
  de torque e a constante de velocidade de um motor.
- **Motivo:** é a fonte da relação física que eu tinha usado para estimar o torque do motor a
  partir do $K_v$ fornecido pelo fabricante — esse trecho foi removido do texto atual da
  Seção 2.2, mas a relação pode valer a pena reintroduzir.
- **Como usar:** citar se você decidir reintroduzir o argumento $K_t \times K_v$ na introdução
  reescrita da Seção 2.2, ou em qualquer outro ponto que faça essa estimativa de torque.

---

## Material didático (UFMG)

### `braga2020a` — Braga e Michel, *Aula 04 — Incerteza de Medição* (DELT/UFMG, 2020)
- **Resumo:** material didático da disciplina de instrumentação do DELT/UFMG, sobre teoria de
  incerteza de medição.
- **Motivo:** base teórica para o tratamento de incertezas previsto no Capítulo 4
  (Resultados), que atende ao objetivo específico (iv) da Introdução.
- **Como usar:** citar no Capítulo 4, ao introduzir o tratamento de incerteza de medição
  (propagação de incerteza, incerteza combinada, etc.).

### `braga2020b` — Braga e Michel, *Aula 05 — Caracterização Estática e Calibração*
  (DELT/UFMG, 2020)
- **Resumo:** material didático sobre calibração estática de sensores (curva de calibração,
  não linearidade, erro de calibração).
- **Motivo:** base teórica para a calibração do sensor de corrente e/ou da balança digital, no
  Capítulo 3 ou 4.
- **Como usar:** citar ao descrever o procedimento de calibração do ACS758 ou da balança.

### `delt2026` — DELT/UFMG, *UFMG lança disciplina inovadora em veículos autônomos para
  engenharia* (site do DELT/UFMG)
- **Resumo:** notícia institucional sobre a disciplina de Veículos Autônomos.
- **Motivo:** fonte para o contexto institucional (disciplina que usa o automodelo), citado na
  Introdução.
- **Como usar:** citar na Introdução, Seção "Motivação e Justificativa", junto à menção à
  disciplina de Veículos Autônomos.

### `lsi2026` — LSI/DELT/UFMG, *Laboratórios — LSI* (site do DELT/UFMG)
- **Resumo:** página institucional descrevendo o Laboratório de Sistemas Inteligentes.
- **Motivo:** fonte para a descrição do laboratório na Seção "Local de Realização".
- **Como usar:** citar na Introdução, Seção "Local de Realização".

### `ccdm2021` — CCDM/UFSCar, *Ensaio de tração* (manual de procedimento, 2021)
- **Resumo:** manual de procedimento de ensaio de tração do Centro de Caracterização e
  Desenvolvimento de Materiais da UFSCar.
- **Motivo:** referência técnica para o procedimento de medição de força/tração, possivelmente
  relevante à montagem do ensaio com a balança digital descrita no Resumo do trabalho.
- **Como usar:** citar na Metodologia, ao descrever o ensaio de tração com a balança e as
  rodas em contato com o solo.

---

## Resumo rápido por seção da monografia

- **Seção 2.1 (O Automodelo):** `kyosho`, `nakashima2021`.
- **Seção 2.2, introdução:** `motioncontroltips_kt` (se reintroduzir o argumento $K_t$),
  `bomfim2021`, `monteiro2016`.
- **Seção 2.2.1 (IMU):** `invensense_mpu`, `dumitrascu2020`.
- **Seção 2.2.2 (SS41F/41G):** `honeywell_ss41f`.
- **Seção 2.2.3 (INA240):** `ti_ina240_2` (ou `ti_ina240`), `yge_esc`, `meisner2021`.
- **Seção 2.2.4 (ACS758/ACS712):** `allegro`, `yge_esc`, `sharma2019`, `bldynomega`,
  `meisner2021`, `liu_kriging`.
- **Seção 2.2.5 (Síntese):** `theys2021`.
- **Figura 2.1:** `gatorlamination2026` (pendência de licença — ver `TODO_VERIFICAR.md`).
- **Capítulo 3 (Metodologia, ainda não escrito):** `arduino_due`, `braga2020b`, `borges2016`,
  `ccdm2021`.
- **Capítulo 4 (Resultados, tratamento de incertezas):** `braga2020a`, `braga2020b`.

---

## Revisão complementar — fontes brasileiras (verificadas no texto integral)

Busca feita em outubro de 2026, priorizando fontes brasileiras, conforme o `GUIA_ESTILO_ESCRITA.md`
(seção 8) e o modelo da UFMG. Para cada fonte, indico o que foi verificado diretamente no PDF e
em qual parte do texto ela serviria. Nada foi inserido no `.bib` nem no texto, como combinado.

### Santin, M.; Bueno, E. — *Sistema para controle de velocidade de motor brushless em malha fechada*
- **Veículo:** *Ignis*, v. 7, n. 3, p. 119–127, set./dez. 2018 (periódico brasileiro, UNIARP).
- **Conteúdo verificado:** controle PI de velocidade de motor brushless em malha fechada, com
  sensores de efeito Hall servindo à comutação e como realimentação de velocidade.
- **Uso sugerido:** Seção 2.2.2 (SS41F/41G), no trecho sobre realimentação de velocidade em
  malha fechada com sensores Hall.

### Gonçalves, T. B. B. — *Implementação de amperímetro por sensor magnético de efeito Hall aplicado a instrumentação de carregadores de baterias tipo íon-lítio*
- **Veículo:** TCC, Engenharia Elétrica, PUC-Rio, 2019 (orientador Alan C. Kubrusly).
- **Conteúdo verificado:** comparação entre shunt de lado baixo e lado alto, com queda de tensão,
  dissipação e impacto no SNR e na exatidão do shunt, e o sensor IMC-Hall, que dispensa shunt e
  é isolado do circuito medido. Tem também uma lista de limitações do shunt em correntes altas.
- **Uso sugerido:** Seção 2.2.3 (shunt/INA240), na análise de dissipação e de SNR, e Seção 2.2.4
  (Hall), no trecho sobre isolamento. Observação: é um TCC, portanto de menor peso que um artigo.

### Rangel, D. Á. — *Modelagem e controle de velocidade do motor CC sem escovas aplicado a veículos elétricos*
- **Veículo:** TCC, Engenharia Elétrica, UNIPAMPA, Alegrete, 2015 (orientador Felipe Bovolini
  Grigoletto).
- **Conteúdo verificado:** modelagem de motor brushless para veículos elétricos a partir de curvas
  de torque por velocidade e de eficiência por torque, com sequência de acionamento dos sensores
  Hall e medição de correntes de fase em simulação e em bancada.
- **Uso sugerido:** Síntese Comparativa (Seção 2.2.5), como precedente nacional da relação entre
  torque, corrente de fase e velocidade em motores brushless de veículos elétricos.

### Bueno, A. G.; Romano, R. A. — *Filtro complementar aplicado à medida de inclinação de plataformas móveis*
- **Veículo:** trabalho da Escola de Engenharia Mauá (EEM/CEUN-IMT), com a autora como aluna de
  iniciação científica. Ano não identificado no documento (metadados do PDF indicam 2011).
  Não foi possível confirmar o veículo de publicação, por isso cite como trabalho acadêmico até
  verificar.
- **Conteúdo verificado:** filtro complementar que combina acelerômetro (baixas frequências) e
  integral do giroscópio (altas frequências), com frequência de corte de 0,5 Hz. O texto mostra
  que o bias do giroscópio gera erro em rampa crescente, que o acelerômetro falha sob aceleração
  do sistema e que a compensação completa do bias exigiria filtros de segunda ordem.
- **Uso sugerido:** Seção 2.2.1 (IMU), no trecho sobre a integração, o filtro complementar e a
  limitação do acelerômetro sob aceleração. É o mais útil para responder às suas anotações sobre o
  filtro e o erro acumulado.

### Mascarenhas, A. W. — *Dispositivo baseado em acelerômetros capacitivos para monitoração de máquinas rotativas*
- **Veículo:** tese de doutorado, Engenharia Elétrica, UFCG, 2006 (orientadores Antônio Marcus
  Nogueira Lima e Cursino Brandão Jacobina). Repositório: `bdtd.ufcg.edu.br`.
- **Conteúdo verificado no resumo e na introdução:** um dispositivo com acelerômetros capacitivos
  fixados a um disco solidário ao eixo calcula o conjugado de motores de indução e de relutância
  variável a partir de acelerações tangenciais. O resultado é comparado com um torquímetro
  comercial.
- **Uso sugerido:** Seção 2.2.1 (IMU), como precedente nacional de estimativa de torque a partir
  de aceleração, com a ressalva de que mede a aceleração no eixo girante e não no chassi.

### Fontes encontradas, mas não verificadas no texto integral
- **Meyer, I. Z. L. (UFMG, 2019)** — caracterização de motores brushless de pequeno porte para
  VANT, com medição de rotação, torque, temperatura, corrente e tensão. Só o resumo foi lido, pois o
  repositório da UFMG não respondeu. Vale verificar antes de citar, por ser a bancada mais próxima
  da sua metodologia.
- **Bomfim, L. K. S. (UnB, 2021)** — já na lista original. O texto foi verificado: a IMU serve ao
  controle de guinada e a odometria é infravermelha, sem medição elétrica.
- **Dissertação da UFRJ/COPPE sobre integração de sinais de aceleração e velocidade angular** —
  tema de deriva de integração, sem verificação do texto nem do autor exato.
- **Adinolfi, Kuga, Oliveira e Souza (SAE 2012-36-0513)** — IMU com GPS e filtro de Kalman para
  velocidade de veículo. Os autores não puderam ser confirmados, então não recomendo citar sem
  checar o artigo original.
- **Trabalho UTFPR (2013)** — substituição de encoders ópticos por sensores Hall em motor CC.
  Encontrado no CAPES/Educapes, sem leitura integral.

### Lacuna identificada
Não encontrei nenhuma fonte brasileira verificada sobre ACS712 ou ACS758 aplicados a motor
brushless, nem sobre comparação de shunt e Hall sob chaveamento PWM. O TCC da PUC-Rio é o mais
próximo, mas trata de carregadores de bateria. Para essa parte, a fundamentação continuará
dependendo do datasheet do fabricante e de fontes internacionais, o que vale mencionar ao
orientador.
