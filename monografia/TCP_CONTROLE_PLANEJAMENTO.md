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

**Sem a redução i.** O estimador e o mestre usam apenas o produto identificado dos dados:
a caracterização estática fornece diretamente a relação força–corrente
$F = G_F\,(I - I_0(u))/u$, com $G_F = 0{,}382$ N/(A/u) ajustado pela origem sobre a
descida ($R^2 = 0{,}984$, $n = 56$). O torque estimado é $\hat{T} = K_T (I - I_0(u))/u$
com $K_T = G_F\,r_\mathrm{ef} = 0{,}0287$ N·m/(A/u). Nenhum valor de i (nem de $K_t$)
entra no projeto — o que o sistema precisa conhecer está todo nos ensaios.

**Escrava** (planta local linearizada $K_\mathrm{loc} = \partial I/\partial u \approx 153$
A/u no ponto nominal, $\tau = 0{,}25$ s, θ ≈ 0):
- λ₂ = τ = 0,25 s (malha tão rápida quanto a planta permite)
- PI₂: $T_{i2} = 0{,}25$ s; $K_{p2} = \tau/(K_\mathrm{loc}\lambda_2) \approx 6{,}5\times10^{-3}$ u/A
- **Caminho direto também no comando**: $u = u_\mathrm{ff} + \mathrm{PI}_2$, com
  $u_\mathrm{ff}$ da inversão da curva estática (lição da simulação: sem ele, o PI precisa
  de integral para segurar $u$ e o transiente destrói o estimador).

**Mestra** (planta = escrava fechada × conversão $K_T/u$):
- λ₁ = 1,5 s — origem: a **regra de separação da cascata** dos slides (mestre 3 a 10 vezes
  mais lento que a escrava; adotado 6× λ₂), confirmada na simulação.
- Ganho programado (linearização, slide): $K_{p1}(u) = \lambda_2 u/(K_T\lambda_1)
  \approx 0{,}69$ A/(N·m) no nominal; $T_{i1} = 0{,}25$ s.
- **Filtro de referência** da entrada do mestre (rampa de 0,6 N·m/s) e **filtro do
  estimador** (0,6 s): lição da simulação — o estimador é quase-estático e pica quando $I$
  e $u$ desbalanceiam; o mestre não pode ver esses picos.
- **Estimador limitado à faixa validada** (0 a 3,35 N·m): lição da simulação — transientes
  produziam leituras impossíveis; o estimador só é válido onde foi caracterizado.

**Discretização** (slide "Implementação digital"): $T_s = 10$ ms (≤ $T_i/10$), integração
trapezoidal, **anti-windup por clamping** (output tracking) nos dois PIs — lição da
simulação: com integração condicional, o sistema travava em saturação (deadlock de
windup). Comando limitado à região validada $u \in [0{,}045;\,0{,}21]$ — lição da
simulação: a curva estática de torque **não é monotônica além da aderência** (cai após
u ≈ 0,26); sem o limite, a malha externa entra em realimentação positiva. O limite do
comando à região de aderência é, assim, parte do projeto, não apenas proteção.

## 4. Especificações e resultado da simulação (slide "PSR/PRP")

Simulação da cascata completa em Python com todas as não-linearidades (curva estática
quadrática da corrente, $I_0(u)$, divisão por $u$, seletor, limites do comando, sag de 20%
na planta e deslocamento de $I_0$ como perturbações, $T_s = 10$ ms). Figura:
`Figuras/simulacao_cascata.png`.

| Cenário | Resultado |
|---|---|
| **PSR** (degrau 1,6 → 3,0 N·m) | ess = 0; sobressinal ≈ 25%, **pinado no teto do estimador** (3,35 N·m); acomodação ~5 s |
| **PRP** (sag 20% + $I_0$ +0,3 A, 8–12 s) | desvio máx ≈ 1,0 N·m; recuperação completa com ess = 0 (o integrador mestre corrige o erro de modelo) |
| **Seletor** (pedido 4,5 > limite 3,3 N·m) | segue o limite, sem windup, e retorna ao pedido menor ao liberar |
| Retorno (3,0 → 1,6 N·m) | ess = 0 |

Leitura honesta: o sobressinal residual é o preço do estimador quase-estático; dentro das
especificações de um controle de tração (malha interna de um sistema cujo referencial vem
de um perfil de aceleração), e declaramento como limitação.

## 5. Validação

Concluída (esta simulação). Figura gerada; pendente apenas a escrita do Cap. 4.

## 6. Mapa para o Cap. 4 (quando ela aprovar)

- 4.1–4.3 (bancada, vazio, curva estática): reescritos com o ajuste direto $G_F$ (sem i,
  sem $K_t$): a regressão de validação passa a ser $F = G_F (I - I_0(u))/u$ pela origem,
  $R^2 = 0{,}984$;
- 4.4 Dinâmica: como corrigido (τ = 0,25 s, âncora no início elétrico);
- **4.5 A malha de controle** (cascata): 4.5.1 variáveis e enquadramento (seção 1); 4.5.2
  estrutura — cascata com estimador inferencial, caminho direto duplo, seletor de
  aderência (seções 1–2, com as respostas: seletor, anti-windup, origem do λ₁); 4.5.3
  projeto — ganhos, filtros e limites, cada um com a justificativa que a simulação
  motivou (seção 3); 4.5.4 PSR/PRP e a figura da simulação (seção 4).

**Decisões confirmadas pela autora**: cascata, simulação. **Pendente de confirmação**:
nenhuma — pronto para escrever o Cap. 4 sobre este esqueleto.
