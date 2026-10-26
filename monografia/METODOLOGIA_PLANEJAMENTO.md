# Planejamento de Escrita — Capítulo 3 (Metodologia) — v5

Diretrizes do modelo (`modelo_PFC_latex.pdf`): capítulo auto-contido (leitor reproduz sem
consultar referências); justificar cada escolha com alternativas e critérios; **nunca invocar
conceito antes de defini-lo** (sem referências para frente); anunciar o que será feito antes de
trechos longos; ser consistente no tempo verbal.

**Storytelling do capítulo**: seguir a cadeia da medida na ordem em que ela acontece —
o que se mede (força) → como se mede (montagem) → correções da montagem (ângulo, raio) →
a outra grandeza (corrente) → como se comanda e registra (degraus/CSV) → o ritual de cada
medida (protocolo) → tratamento (consolidação) → quanto se pode confiar (incertezas).

Fatos confirmados pela autora (26/10, noite):
- Cabo 126 cm de cada lado; balança 15 cm do chão; engate 28 cm; 3× cada → sen θ = 13/126 →
  θ = 5,9°; cos θ = 0,995 (≤ 0,53%).
- Gancho na estrutura traseira, ACIMA do eixo de transmissão.
- Tara nos 3 s de neutro; força nos s 7, 8, 9; ponto = média; idem descida; vídeo.
- Massa total 6,640 kg (3×). [efeito: μ do Cap. 4 = 0,80]
- ACS758ECB-200B a 3,3 V → 6,6 mV/A; offset 1,65 V; 12 bits → 122 mA/LSB.
- **Calibração da balança com pesos padrão**: 0,5 kg → 0,490; 1,0 kg → 0,980; 1,5 kg →
  1,470 — erro sistemático de 10 g a cada 0,5 kg (≈ −2%); resolução 10 g.
- Script de degraus (`teste_throttle.py`) do orientador, executa no Pi, via ssh do notebook.
- Verificação bancada do sensor: 0–6 A, regressão y = 1,0742x, desvios ±7% (corrigíveis em
  software).
- Escadas: força+vídeo 97→117 e 117→97; contínua 100 Hz 98→119 e 120→113.

---

## 3.1 O Ensaio de Tração Estática

**P1 (abertura — define tudo que as próximas seções usam).** Caracterizar o propulsor exige
medir, simultaneamente, a força de tração e a corrente elétrica — a curva que se busca é
torque × corrente. A força só se manifesta em movimento; para medê-la em condição
estacionária, o veículo é ancorado: impedido de se deslocar, a reação da ancoragem iguala a
tração desenvolvida, dispensando dinamômetro. **Definir aqui kgf** (travessão): a balança é
graduada em quilogramas, mas o que ela mede quando o gancho é puxado é uma força, expressa
como o peso da massa equivalente — 1 kgf = 9,81 N; por isso a leitura em quilogramas, com o
gancho tracionado horizontalmente pela reação da ancoragem, é força de tração e não peso.
Fecho anunciador: o torque na roda é obtido da força pela roda (Seção 3.3) e a corrente pela
cadeia elétrica (Seção 3.4).

**3.1.1 Configuração de ancoragem — 1 parágrafo.** Gancho da balança engatado na estrutura
traseira do veículo, acima do eixo de transmissão; cabo de 126 cm em cada lado da balança;
balança suspensa, a 15 cm do chão no lado do padrão e 28 cm no engate; dimensões anotadas
3×. FIGURA: fotografia da montagem.

**3.1.2 Padrão de força e sua calibração — 2 parágrafos.**
- P1: balança digital de mala com gancho; **calibração com pesos padrão** antes do ensaio:
  0,500 kg lidos como 0,490; 1,000 como 0,980; 1,500 como 1,470 — erro sistemático de 10 g
  por 0,5 kg (≈ −2%), registrado e usado na Seção 3.6; resolução de 10 g.
- P2: alternativas consideradas e critério de escolha (ver Relatório Parcial 2): dinamômetro
  comercial — inviável em custo e disponibilidade para escala 1/8; célula de carga com
  registrador — exigiria eletrônica adicional e fica como proposta de continuidade
  (viabilizaria a medição dinâmica); a balança de mala é o melhor compromisso custo–
  simplicidade–faixa (< 6 kgf).

**3.1.3 Massa adicional — 1 parágrafo.** Conjunto a 6,640 kg (massa adicional sobre o CG),
anotado 3×; função exclusivamente condicionante — aumenta a carga normal sobre os pneus e o
atrito disponível, retardando a patinagem; não entra no cálculo do torque; a condição de
carregamento integra a especificação do ensaio.

## 3.2 Geometria do Cabo e o Efeito Cosseno — 1 parágrafo

A tensão medida pela balança atua ao longo do cabo; a grandeza de interesse é a componente na
linha de tração, F·cos θ. Das dimensões medidas (3×): sen θ = (28 − 15)/126 → θ = 5,9° →
cos θ = 0,995 — a correção máxima, 0,53%, fica abaixo da incerteza de leitura da balança, e
o efeito do ângulo é desprezado.

## 3.3 Medida do Raio Efetivo da Roda — 1–2 parágrafos

Método roll-out: marcas no pneu e no solo; a roda é movimentada 5 vezes com o veículo
encostado na parede, o que garante o rolamento reto; 3 anotações independentes; L = 236 cm →
r_ef = L/(2π·5) = 0,0751 m, contra 80 mm nominais (pneu novo, sem carga) — deflexão de 6,1%
sob carga. Fecha a cadeia anunciada em 3.1: o torque na roda é
\begin{equation}
T_\mathrm{roda} = F\,r_\mathrm{ef},
\end{equation}
e o uso do raio nominal injetaria 6% de erro sistemático em todo o resultado.

## 3.4 Instrumentação Elétrica e Aquisição

**3.4.1 Sensor de corrente — 1 parágrafo.** ACS758ECB-200B em série na alimentação do
conjunto ESC–motor; efeito Hall, isolado galvanicamente; alimentado a 3,3 V pelo Arduino
Due; sensibilidade ratiométrica 6,6 mV/A a 3,3 V (10 mV/A a 5 V); saída 1,65 V em corrente
zero; filtro RC de ~24 Hz; ADC de 12 bits → resolução de 122 mA por LSB. Dois firmwares:
básico (100 amostras consecutivas ~1 ms por ponto, 1 ponto/s) e rápido (período de 10 ms,
~100 Hz). [Citações de amostragem na rodada futura.]

**3.4.2 Verificação em bancada — 1 parágrafo.** Antes do ensaio, o sensor foi confrontado com
um multímetro de referência, com fonte de 0 a 6 A; resposta linear em toda a faixa, regressão
y = 1,0742x (multímetro x, sistema y); desvios sistemáticos de ±7%, compensáveis por fator de
correção em software. O sensor fica validado para o monitoramento.

**3.4.3 Geração dos degraus e registro em CSV — 2 parágrafos.**
- P1 (o comando): o script de degraus, disponibilizado pelo orientador, executa no Raspberry
  Pi e é acionado remotamente por ssh do notebook:
  `ssh alunos@raspberrypi.local "python3 teste_throttle.py <ângulo> <duração>"`.
  **Definir neutro** (travessão): o comando de 95°, que corresponde ao pulso de 1,5 ms do
  padrão de rádio-controle, para o qual o ESC mantém o motor parado; o script coloca o ESC em
  neutro, aplica o degrau pela duração programada e retorna ao neutro. O gerador de pulsos
  (PCA9685) opera na faixa de servo 90–180°; usa-se o comando normalizado u = (θ−95)/85.
- P2 (o registro): um script de automação local percorre a escala de degraus em um laço,
  substituindo ângulo e duração a cada iteração e lançando o comando ssh; em paralelo, a
  serial do Arduino é lida e cada amostra — tempo de ensaio, tempo dentro do degrau, ângulo e
  corrente — é gravada em CSV, um bloco por degrau. No terminal, mesmo com a aquisição a
  100 Hz, imprime-se somente a média de cada segundo (t = 1, 2, … 15 e a corrente média
  associada); é essa linha, com horário, que aparece no vídeo ao lado do display da balança.

**3.4.4 Retempo das amostras a 100 Hz — 1 parágrafo.** As amostras chegam pela serial em
rajadas de ~10 com o mesmo timestamp (blocos de 100 ms), porque o envio serial bufferiza; a
ordem de chegada preserva a sequência de aquisição, de modo que o tempo é reconstruído por
índice — a k-ésima amostra do arquivo ocorre em t = k×10 ms, com k = 0, 1, 2, … —, e cada
degrau de 15 s gera ~1550 amostras sem perda de resolução temporal.

## 3.5 Procedimento Experimental

**3.5.1 Checklist pré-ensaio — 1 parágrafo.** Bateria LiPo 2S carregada — o corte de baixa
tensão do ESC bloqueia o motor quando a tensão cai; bateria do Raspberry carregada — o
step-down que a alimenta tem amostragem da tensão; notebook conectado à rede do Pi.

**3.5.2 Escadas de comando — 1 parágrafo.** Dois conjuntos: (a) com força anotada e vídeo —
subida 97→117° e descida 117→97°, faixa completa nos dois sentidos; (b) aquisição contínua a
100 Hz — subida 98→119° e descida 120→113°. Degraus de 15 s; neutro de 3 s entre degraus.

**3.5.3 Protocolo de cada degrau — 2 parágrafos.**
- P1 (força): a balança é tarada nos 3 s de neutro entre degraus (a corda relaxa 0,1–0,2 kg
  entre puxadas); após o comando enviado por ssh, aguarda-se 7 s — a resposta de corrente se
  assenta em ~4τ ≈ 7 s, conforme a dinâmica identificada no Cap. 4 — e a força é anotada nos
  segundos 7, 8 e 9; o ponto é a média das três leituras. Mesmo protocolo na descida.
- P2 (vídeo): a sessão é gravada em vídeo, enquadrando o display da balança e o terminal do
  notebook — este último exibindo o horário, o tempo t e a corrente média do segundo; cada
  ponto é lido pausado, quadro a quadro, após o experimento, o que padroniza a leitura,
  elimina erro de pressa e paralaxe e dá rastreabilidade ao valor anotado (o display não tem
  saída elétrica).

**3.5.4 Ensaio em vazio — 1 parágrafo.** Rodas suspensas em caixa, sem contato com a mesa;
mesmos degraus; fornece I₀(u), a corrente sem carga, usada na separação das perdas do modelo.

**3.5.5 Consolidação e validação — 1–2 parágrafos.** Os CSVs da aquisição contínua foram
consolidados por script, com regras objetivas por execução: pico acima de 60 A indica registro
corrompido (falha serial); degrau acima de 100° com pico inferior a 3 A, ou a partir de 99°
com pico inferior a 1 A, indica comando não executado; duração inferior a 10 s, execução
curta; o sentido da escada é inferido pelo arquivo de origem. Das 58 execuções registradas,
54 validadas — subida 98–119°, descida 113–120°; a ausência de descida abaixo de 113° nesta
aquisição é declarada como lacuna (a sessão com força cobre 97–117° nos dois sentidos).

## 3.6 Incertezas de Medição — 3 parágrafos + TABELA

- P1 (Tipo A): dois níveis — dispersão das 3 leituras (s 7–9) dentro de cada ponto e
  dispersão entre as repetições da escada (repetibilidade do método); reportar os dois.
- P2 (Tipo B): balança — resolução 10 g (u = 5/√3 ≈ 2,9 g) **e o erro sistemático de
  calibração de 10 g/0,5 kg, corrigido ou declarado**; leitura em vídeo — ±1 dígito quando
  houver dúvida de legibilidade; corrente — quantização 122 mA (u ≈ 35 mA); verificação em
  bancada — ±7% corrigidos em software, com resíduo declarado.
- P3 (sistemáticas e propagação): θ → cos θ = 0,995 (0,53%); r_ef < 0,5%; T = F·r_ef por
  soma quadrática das componentes relativas. TABELA por faixa de degrau (gerar de
  `pfc kaka.xlsx` + consolidado).

## Resumo do Capítulo — 1 parágrafo
Do que se mede a como se confia: ensaio ancorado → montagem com geometria medida → cosseno
quantificado → raio efetivo → cadeia elétrica verificada em bancada → degraus automatizados
com registro em CSV → protocolo com vídeo e tripla leitura → incertezas em dois níveis.
Ponte ao Cap. 4.

---

## Ordem de escrita (um bloco por vez, autora valida cada)
1. 3.1 P1 (abertura com kgf) + 3.2 (cosseno) — números prontos;
2. 3.3 (roll-out + equação do torque) — pronto;
3. 3.4.2 (bancada) — pronto;
4. 3.4.3 (ssh, neutro, laço, CSV, terminal) — pronto;
5. 3.1.1 + 3.1.2 + 3.1.3 (montagem, calibração da balança, massa) — precisa da foto;
6. 3.5 todo — pronto;
7. 3.4.1 + 3.4.4 (sensor e retempo) — pronto;
8. 3.6 — eu gero a tabela antes;
9. Resumo.
