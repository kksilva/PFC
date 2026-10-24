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
- [ ] Bateria LiPo 2S saudável, carregada; verificar tensão por célula antes
- [ ] Halteres 1 kg ×2 fixados sobre o CG (fita/velcro), massa total anotada (~7,1 kg)
- [ ] Tarar balança 1× por série, em repouso (nunca entre degraus)
- [x] θ: DESPREZÍVEL por decisão (balança suspensa pela alça alinha o eixo à linha de tração; θ residual só da geometria de engate) — ver `PLANEJAMENTO_MONOGRAFIA.md` §3.3, marcado RESOLVIDO em 22/10/2026
- [ ] Notebook na rede do Raspberry; testar `ssh alunos@raspberrypi.local` sem senha
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

