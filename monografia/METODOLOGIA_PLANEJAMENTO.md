# Planejamento de Escrita — Capítulo 3 (Metodologia)

Lista passo a passo do que o capítulo descrevia. **Cada item tem os fatos/valores como estavam
escritos — confira e corrija os que mudaram durante o ensaio** (marque com [OK] ou anote a
correção). Depois reescrevemos item a item no seu estilo.

---

## 3.1 Escolha da Instrumentação e Montagem do Ensaio de Tração Estática

### 3.1.1 Padrão de força
- [ ] Princípio do ensaio ancorado: veículo impedido de se deslocar → força de reação da ancoragem iguala a tração → medida estacionária sem dinamômetro.
- [ ] Padrão adotado: balança digital de mala com gancho, resolução **10 g**.
- [ ] Alternativa rejeitada: célula de carga com registrador (custo/benefício na faixa < 6 kgf; fica como continuidade — viabilizaria medição dinâmica).
- [ ] Alternativa rejeitada: dinamômetro comercial (inviável custo/disponibilidade para 1/8).
- [ ] Descrição da montagem final: **estrutura traseira acima do veículo** à qual o gancho da balança é engatado; balança presa por corda a estrutura fixa (armário/gaveta). **CONFIRMAR a montagem real final** (mudou várias vezes: cadeiras → gaveta → armário; barra anti-rolagem? gancho no para-choque? balança suspensa pela alça?).
- [ ] Equação T_roda = F·r_ef (referencia a medição do raio efetivo).
- [ ] FIGURA: fotografia da montagem final.

### 3.1.2 Massa adicional e aderência
- [ ] Massa adicional: **três halteres de 0,5 kg** sobre o CG → massa total **~7,1 kg**. **CONFIRMAR** (teve época com 2 halteres de 1 kg; peso vertical medido 5,140 kg — conferir composição real usada no ensaio definitivo).
- [ ] Papel da massa: apenas condicionante (aumenta atrito disponível, retarda patinagem); não entra no cálculo do torque.
- [ ] Massa integra a especificação do ensaio (tração máx. transferível depende dela).

## 3.2 O Ângulo do Cabo (efeito cosseno)
- [ ] Princípio: balança mede a tensão no cabo; a componente útil é F·cos θ; θ = ângulo entre cabo e linha de tração.
- [ ] Decisão: θ desprezível — balança suspensa pela alça alinha o eixo ao cabo; θ residual só da geometria de engate.
- [ ] Evidência experimental: peso do veículo medido na vertical **5,140 kg** e na horizontal (cabo esticado ao máximo) **5,130 kg** → concordância 0,19% → θ ≈ 0.
- [ ] Decisão registrada de **não medir θ** em cada ensaio. **CONFIRMAR** se permanece válida.

## 3.3 Medida do Raio Efetivo da Roda (roll-out)
- [ ] Método: distância percorrida em **5 voltas** completas da roda, marcação no piso: **L = 236 cm**.
- [ ] Resultado: r_ef = L/(2π·5) = **0,0751 m** vs. nominal **80 mm** (pneu novo sem carga); deflexão 6,1%; incerteza < 0,5%.
- [ ] Justificativa: usar r_ef (e não o nominal) em T = F·r.

## 3.4 Cadeia de Aquisição e Geração de Degraus

### 3.4.1 Aquisição da corrente
- [ ] Sensor ACS758 em série no ramo de alimentação, alimentado em **3,3 V pelo Arduino Due**, sensibilidade **6,6 mV/A** (?) e offset ratiométrico; ADC 12 bits do Due.
- [ ] Filtro RC ~**24 Hz** na entrada.
- [ ] Firmware básico: **100 amostras ADC consecutivas (~1 ms) por ponto, 1 ponto/s** (ensaio com forças anotadas).
- [ ] **CONFIRMAR sensibilidade** (depende da versão do ACS758: ±50/100/150/200 A têm sensibilidades diferentes).

### 3.4.2 Ensaio dinâmico a 100 Hz
- [ ] Firmware rápido (`Sensor_de_Corrente_ACS758_fast.ino`): período **10 ms** (~100 Hz), usado no ensaio "cego".
- [ ] Regras de amostragem citadas (10–30× a banda; 10–20 amostras no tempo de subida) — **reativar citações depois**.
- [ ] Particularidade: buffer USB → amostras recebidas em rajadas de ~10 com timestamps iguais; retempo t = k×10 ms pela ordem do arquivo; ~1550 amostras/bloco de 15 s.

### 3.4.3 Geração dos degraus
- [ ] Raspberry Pi + PCA9685 (padrão servo 90–180°, neutro 95°), normalização u = (θ−95)/85.
- [ ] Dois modos: confirmado via ssh (com telemetria) e **cego** (disparo autônomo ancorado na resposta elétrica da corrente, sem depender da rede).

## 3.5 Procedimento Experimental

### 3.5.1 Checklist pré-ensaio
- [ ] Tensão da LiPo 2S em repouso ≥ **7,7 V** (cheia 8,4 V; LVC do ESC abaixo disso).
- [ ] Bateria do Raspberry Pi carregada (brown-out medido: step-down em **4,0 V** vs 5,3 V → queda da rede).
- [ ] Notebook na rede do Pi (SSID correto), ssh sem senha funcionando.

### 3.5.2 Protocolo dos degraus
- [ ] **Tara da balança antes de cada degrau** (drift da corda ~0,1–0,2 kg entre degraus); registro da leitura de repouso antes de zerar.
- [ ] Degrau de **15 s**; anotação da força nos **últimos 3 s** (janela 7–10 s? **confirmar janela** — havia versões 7–10 s e 12–15 s).
- [ ] Escada: subida **95→119°**, descida **120→113°**. **CONFIRMAR os extremos reais**.
- [ ] Pausa entre degraus (60 s? neutro de 2 s? — **confirmar**).

### 3.5.3 Ensaio em vazio
- [ ] Roda(s) suspensa(s), degraus 97→117° → I₀(u) (corrente sem torque). **Confirmar configuração** (caixa suspensa? com/sem massa?).

### 3.5.4 Consolidação e validação
- [ ] Script consolidador; regras: pico > **60 A** = corrompido; degrau > 100° com pico < **3 A** ou ≥ 99° com pico < **1 A** = sinal fraco; duração < **10 s** = curto.
- [ ] **58 registradas → 54 validadas**; correção do sentido pelo nome do arquivo.
- [ ] Cobertura: subida 98–119°, descida 113–120°; lacuna: descida 98–112°.

## 3.6 Incertezas de Medição
- [ ] Tipo A: repetibilidade (desvio-padrão das 4 repetições por degrau) — **falta gerar os valores da planilha**.
- [ ] Tipo B: resolução da balança (**10 g**) e do ADC/sensor (**~122 mA** — confirmar com a sensibilidade correta).
- [ ] Combinada u_c = √(u_A² + u_B²); expandida **U = 2·u_c** (k = 2, ~95%).
- [ ] Propagação relativa em T = F·r_ef.
- [ ] TABELA de incertezas por degrau (gerar do `pfc kaka.xlsx` + consolidado).

## Resumo do Capítulo
- [ ] Fecho amarrando metodologia → Cap. 4.
