# Planejamento de Escrita — Capítulo 3 (Metodologia) — v2

Fatos corrigidos pela autora (26/10, noite):
- Cabo de 126 cm amarrado de cada lado da balança; balança a 15 cm do chão; cabo a 28 cm do
  chão no engate do veículo; medidas anotadas 3×.
- Gancho da balança engatado em estrutura traseira do veículo, ACIMA do eixo de transmissão.
- Tara feita nos 3 s entre um degrau e outro.
- Protocolo: após o comando, espera 7 s; força anotada nos segundos 7, 8 e 9; média dos 3.
- Mesmo protocolo na descida.
- Tudo gravado em vídeo; valores anotados com calma após o experimento.
- Massa adicional: outro peso (não halteres), total do conjunto **6,640 kg**, anotado 3×.
- Sensibilidade da leitura considera alimentação de 3,3 V (ex.: ACS758 ±200 A: 10 mV/A em 5 V
  → 6,6 mV/A em 3,3 V — confirmar versão do chip).
- Ensaio em vazio: rodas suspensas em caixa, sem tocar a mesa.
- Roll-out: pneu e solo marcados; roda movimentada 5× com o carrinho encostado na parede
  (alinhamento garantido); anotações 3×.

Cálculo novo (da geometria): sen θ = 13/126 → θ = 5,9°; cos θ = 0,995; correção ≤ 0,53%.

EFEITOS COLATERAIS a corrigir em outros arquivos ao reescrever:
- TODO item 12: μ aparente 0,75 → **0,80** (52 N / 65,1 N com 6,640 kg).
- Cap. 4: referências a "7,1 kg" → 6,640 kg; μ = 0,80.

---

## Divisão proposta (7 seções, subseções curtas)

### 3.1 Princípio do Ensaio de Tração Estática e Montagem
Parágrafo de abertura: o que se mede (força + corrente) e por que o ensaio ancorado (reação =
tração; sem dinamômetro). **3 subseções:**

**3.1.1 Configuração de ancoragem.** Estrutura traseira do veículo com gancho acima do eixo de
transmissão; cabo de 126 cm em cada lado da balança; balança suspensa (15 cm do chão no lado
do padrão, 28 cm no lado do veículo); medidas repetidas 3×. FIGURA: foto da montagem final.

**3.1.2 Padrão de força e registro em vídeo.** Balança de mala com gancho (resolução 10 g);
registro em vídeo de todos os degraus; anotação posterior com calma — justificativa: o display
não tem saída; o vídeo preserva as 3 leituras de cada ponto. (Célula de carga + registrador =
proposta de continuidade; dinamômetro comercial inviável.)

**3.1.3 Massa adicional.** Total 6,640 kg (veículo + peso adicional sobre o CG), anotado 3×;
função exclusivamente condicionante (aumenta atrito disponível, retarda patinagem); não entra
no cálculo do torque; integra a especificação do ensaio.

### 3.2 Geometria do Cabo e o Efeito Cosseno
Um bloco só (sem subseções): a balança mede a tensão no cabo; a componente útil é F·cos θ;
cálculo da seção: sen θ = 13/126 → θ = 5,9° → cos θ = 0,995 → erro máximo 0,53%, dentro da
incerteza de leitura → θ desprezado **por medida**, não por hipótese. Evidência independente
de apoio: peso do conjunto medido na vertical (5,140 kg antes da massa adicional) e na
horizontal esticando o cabo concordam dentro de 0,2%.

### 3.3 Medida do Raio Efetivo da Roda
Um bloco: método roll-out com marcações no pneu e no solo; 5 voltas com o veículo encostado
na parede (rolamento reto garantido); 3 anotações independentes; L = 236 cm → r_ef = 0,0751 m
vs nominal 80 mm (deflexão 6,1%); usar r_ef em T = F·r_ef.

### 3.4 Cadeia de Aquisição e Geração de Degraus
**3.4.1 Medição da corrente.** **CONFIRMADO: ACS758ECB-200B (±200 A)** em série na
alimentação, alimentado em 3,3 V pelo Due; sensibilidade ratiométrica 10 mV/A a 5 V → **6,6 mV/A
a 3,3 V**; saída em corrente zero = Vcc/2 = 1,65 V; filtro RC ~24 Hz; ADC 12 bits → resolução
**122 mA/LSB**, incerteza tipo B de quantização ≈ 35 mA (0,1–0,3% na faixa do ensaio);
firmware básico (100 amostras ~1 ms por ponto, 1 ponto/s).

**3.4.2 Ensaio dinâmico a 100 Hz.** Firmware rápido (período 10 ms); regras de amostragem
(reativar citações depois); rajadas do buffer USB e retempo por índice (t = k×10 ms).

**3.4.3 Geração dos degraus.** Raspberry Pi + PCA9685 (90–180°, neutro 95°); u = (θ−95)/85;
dois modos: confirmado via ssh e cego (ancorado na resposta elétrica).

### 3.5 Procedimento Experimental
**3.5.1 Checklist pré-ensaio.** LiPo ≥ 7,7 V em repouso; bateria do Raspberry carregada
(brown-out documentado: step-down em 4,0 V vs 5,3 V); notebook na rede do Pi.

**3.5.2 Protocolo do degrau.** Tara nos 3 s entre degraus (drift da corda 0,1–0,2 kg);
após o comando, espera de 7 s (≈4τ da dinâmica identificada — retomar no Cap. 4); força
anotada nos segundos 7, 8 e 9; ponto = média das 3 leituras; mesmo protocolo na subida e na
descida; sessão gravada em vídeo.

**3.5.3 Escadas de comando (DUAS SESSÕES DISTINTAS — não misturar no texto).**
(a) Ensaio com força anotada + vídeo: subida **97→117°** e descida **117→97°** (faixa completa
nos dois sentidos → histerese com força cobre tudo); duração 15 s por degrau; tara nos 3 s de
neutro entre degraus.
(b) Ensaio cego (dinâmica 100 Hz, sem rede): subida **98→119°** e descida **120→113°** (queda
da rede interrompeu a descida em 113° — lacuna só desta sessão).

**3.5.4 Ensaio em vazio.** Rodas suspensas em caixa, sem contato com a mesa; mesmos degraus;
fornece I₀(u).

**3.5.5 Consolidação.** Regras (60 A / 3 A / 1 A / 10 s); 58 registradas → 54 validadas;
cobertura e lacunas.

### 3.6 Incertezas de Medição
Tipo A: dispersão das 3 leituras (7–9 s) por ponto + repetibilidade entre as repetições da
escada; Tipo B: resolução da balança (10 g), resolução do ADC, leitura humana do display;
componentes sistemáticas pequenas: θ (0,53%) e r_ef (<0,5%); u_c, U = 2u_c (k=2); propagação
em T = F·r_ef. TABELA por faixa de degrau (gerar de `pfc kaka.xlsx`).

### Resumo do Capítulo
Fecho curto: montagem → geometria → raio → cadeia → protocolo → incerteza; ponte ao Cap. 4.

---

## Ordem de escrita sugerida (um passo por vez, você valida cada)
1. 3.1.1 + 3.1.2 (montagem e vídeo) — dependem só das fotos;
2. 3.2 (cosseno) — já tem todos os números;
3. 3.3 (roll-out) — números fechados;
4. 3.4 (cadeia) — confirmar sensibilidade do ACS758 e versão do chip;
5. 3.5 (procedimento) — confirmar extremos das escadas e pausa;
6. 3.6 (incertezas) — eu gero a tabela da planilha;
7. Resumo.
