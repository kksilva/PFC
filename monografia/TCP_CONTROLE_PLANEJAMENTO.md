# Planejamento do Controle — Cap. 4 (reescrita) e §4.4

Base teórica: slides de TCPI (prof. Raffo, DELT/UFMG, pasta `~/PFC/TCPI`): Variáveis
Básicas, PID 1–2, Síntese Direta, IMC, Linearização, Cascata/Inferencial/Seletivo/Split,
PSR/PRP, Alocação de Polos. Modelo da planta: dados identificados (ensaio 100 Hz +
caracterização estática).

---

## 1. Enquadramento do problema (slides "Variáveis Básicas")

O controle de torque/corrente do propulsor se enquadra, na classificação das variáveis
básicas, no mesmo perfil do **controle de vazão**: dinâmica rápida com tempo morto
desprezível (τ = 0,25 s, θ ≈ 0 — identificados), perturbações frequentes porém pequenas
(sag da bateria, variação de I₀ com a temperatura) e **ruído de alta frequência na medição**
(quantização de 122 mA + chaveamento do ESC). O slide recomenda, para vazão, controle
regulatório com realimentação rápida — é o nosso caso: a malha interna de corrente.

**Variáveis (definir no texto, na notação dos slides):**
- Variável controlada primária (CV1): torque na roda $T$ — **não mensurável embarcada**;
- Variável controlada secundária (CV2): corrente de bateria $I$ — mensurável (ACS758);
- Variável manipulada (MV): comando $u$ (0–1, normalizado);
- Perturbações $q$: sag da bateria (tensão), temperatura do pneu/bateria, variação de I₀;
- Referência $y_r$: torque desejado $T_\mathrm{ref}$.

## 2. Estrutura escolhida — cascata com realimentação inferencial (slide "Cascata")

A cascata é a estrutura do slide, com a motivação dele: *"a ação corretiva da malha simples
age apenas após a variável controlada desviar; a cascata mede uma variável auxiliar,
sensível às perturbações mais rapidamente que a controlada primária"* — aqui, a corrente
responde em 0,25 s e o torque estimado (via modelo) sem sensor adicional.

- **Malha escrava (interna)**: CV = corrente $I$; controlador PI₂. Planta identificada
  $G_1(s) = 120/(0{,}25s+1)$ (ensaio a 100 Hz).
- **Malha mestra (externa)**: CV = torque **estimado** $\hat{T} = C(I - I_0(u))/u$
  (estimador validado, r² = 0,962) — é o **controle inferencial** do slide: a variável
  primária é reconstruída por modelo quando não há sensor on-line; controlador PI₁; saída =
  $I_\mathrm{ref}$ (set-point da escrava).
- **Pré-alimentação de $y_r$** (esquema geral do slide PSR/PRP): o *feedforward* da inversa
  estática entra como pré-alimentação da referência na escrava,
  $I_\mathrm{ref} = I_\mathrm{ff} + I_1$, com $I_\mathrm{ff}$ da curva estática — lineariza
  o caminho e deixa ao mestre apenas a correção do erro de modelo (slide "Linearização":
  pré-alimentação da referência lineariza a malha).
- **Controle seletivo (override)** do slide "Seletivo": o limitador de aderência entra como
  seletor de mínimo — $T_\mathrm{ref}$ efetivo = mín($T_\mathrm{ref}$, $T_\mathrm{max}$)
  com $T_\mathrm{max}$ da curva característica (3,9 N·m quente, 2,4 N·m frio). Função de
  segurança e de validade do modelo, como no slide.
- Perturbação $q$ (sag, temperatura): **não mensurável** no veículo → rejeição pela
  realimentação (mestre lento + escrava rápida), sem pré-alimentação de $q$ (conforme o
  esquema geral: pré-alimentação de q só "se q for medido ou estimado" — não é o caso).

## 3. Projeto dos controladores (slides "Síntese Direta" e "IMC")

Síntese direta/IMC (Garcia & Morari): escolhe-se o comportamento de malha fechada desejado
$F(s) = 1/(\lambda s + 1)$; o controlador resulta da inversa do modelo filtrada,
$C = Q/(1 - Q\hat{G})$ com $Q = \hat{G}^{-1}F$. O parâmetro $\lambda$ explicita o
compromisso desempenho/robustez (vantagem do slide).

**Escrava** (planta $\hat{G} = K/(\tau s+1)$, $K = 120$ A/u, $\tau = 0{,}25$ s, θ ≈ 0):
- λ₂ = τ = 0,25 s (malha tão rápida quanto a planta permite)
- PI₂: $T_{i2} = \tau = 0{,}25$ s; $K_{p2} = \tau/(K\lambda_2) = 8{,}3\times10^{-3}$ u/A
- Malha fechada da escrava ≈ $1/(\lambda_2 s + 1)$.

**Mestra** (planta = escrava fechada × conversão torque–corrente, ganho depende de u):
- Do estimador: $\hat{T} = \frac{C}{u}(I - I_0)$, $C = \eta i K_t/r_\mathrm{ef} \approx 0{,}40$ N·m
  (com η = 0,579). Ganho da "planta mestra" no ponto nominal u₀ = 0,118:
  $K_o = C/u_0 \approx 3{,}4$ N·m/A, dinâmica ≈ λ₂.
- λ₁ = 4λ₂ = 1 s (regra da cascata: mestre 3–10× mais lenta que a escrava — slide).
- **Ganho programado** (linearização, slide "Linearização"): $K_{p1}(u) = \lambda_2 u/(C\lambda_1)$,
  T_{i1} = λ₂ = 0,25 s. No nominal: $K_{p1} \approx 0{,}074$ u/(N·m)·u... (unidade: A por N·m
  — ajustar no texto).

**Discretização** (slide "Implementação digital"): T_s = 10 ms (firmware rápido gravado;
≤ T_i/10). Integração trapezoidal; anti-windup por clamp (saturnação do comando 0–1 e do
seletor de aderência); rate-limit |du/dt| para proteger a transmissão.

## 4. Especificações de desempenho (slide "PSR/PRP")

- **PSR** (seguimento de referência): degrau de T_ref dentro da faixa de aderência →
  resposta de 1ª ordem com λ₁ = 1 s (63% em 1 s, acomodação ~4 s), sobressinal nulo,
  ess = 0. Feedforward garante que a maior parte do movimento vem do caminho direto.
- **PRP** (rejeição de perturbação): degrau de carga (ex.: queda de tensão da bateria
  modelada como variação de ganho de 20% no caminho da corrente, ou variação de I₀) em
  t = 5 s → rejeição pela escrava em ~3λ₂ ≈ 0,75 s para perturbações no caminho da corrente,
  e pelo mestre em ~3λ₁ para erro de modelo; ess = 0.
- **Robustez** (vantagem IMC do slide): variação de K ±20% e τ ±30% → manter PSR/PRP
  qualitativos; reportar margens ou, minimamente, o varredura paramétrica.

## 5. Validação (antes de escrever o Cap. 4)

1. Simular em Python (ou MATLAB) a cascata completa com não-linearidades (I₀(u), divisão
   por u, seletor de aderência, saturação 0–1) e conferir PSR/PRP;
2. Confirmar regra de separação das malhas (λ₁/λ₂ = 4) na simulação;
3. Gerar as figuras: resposta PSR, resposta PRP, varredura de robustez (3 figuras novas
   substituem as anteriores 4.5/4.6 que a autora removeu).

## 6. Mapa para o Cap. 4 (quando ela aprovar este plano)

- 4.1–4.3 (bancada, vazio, curva estática): como estavam (sem alteração de fundo);
- 4.4 Dinâmica: como corrigido (τ = 0,25 s, âncora no início elétrico);
- **4.5 A malha de controle**: 4.5.1 variáveis e enquadramento (seção 1 acima); 4.5.2
  estrutura em cascata com inferência e seletivo (seção 2); 4.5.3 projeto por IMC com os
  números (seção 3); 4.5.4 PSR/PRP e robustez com as figuras (seções 4–5).

**Decisões a confirmar pela autora**: (a) cascata mestre/escrava + feedforward + seletor
(como neste plano) — coerente com a §2.3 da Proposta, que já diz "a malha organiza-se em
cascata"; (b) λ₁ = 1 s (regra 3–10×); (c) validação por simulação com não-linearidades
antes da escrita.
