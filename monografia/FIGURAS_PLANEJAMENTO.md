# Planejamento — Figuras, Função de Transferência e Resposta ao Degrau (Cap. 4/5)

Ferramenta: **Python com MATLAB Engine** (`matlab.engine`) — os scripts rodam em Python e
chamam o MATLAB R2025b instalado em `/usr/local/MATLAB/R2025b` para o que exige caixa-preta
(ajuste de função de transferência, resposta ao degrau). O pré-processamento dos CSVs fica em
Python puro (pandas/numpy), e as figuras em matplotlib — o MATLAB entra só na identificação e
na simulação.

## 0. Setup (uma vez só)

```bash
cd /usr/local/MATLAB/R2025b/extern/engines/python
python3 setup.py install --user   # expõe matlab.engine ao python3
```
Verificar: `python3 -c "import matlab.engine"`. Fallback, se a engine der problema:
`pip install control` (python-control, sintaxe MATLAB-like: `tf`, `step`, `bode`).

Padrão de uso nos scripts:
```python
import matlab.engine
eng = matlab.engine.start_matlab()          # abre o MATLAB em background
# ... pré-processamento em Python, depois:
m_t = matlab.double(t.tolist()); m_y = matlab.double(y.tolist())
sys1 = eng.tfest(matlab.double(np.column_stack([t, y])), 1.0)   # requer System ID Toolbox
K, tau, theta = ...                          # extrair dos modelos
eng.quit()
```

---

## 1. Figuras do Cap. 4

### FIG 4.1 — Curva característica força × comando (com regiões)
- **Fonte:** `ensaios/pfc kaka.xlsx` (4 repetições × 2 sentidos, degraus 97–117°).
- **Processamento:**
  1. Para cada degrau e sentido: mediana e desvio-padrão das 4 repetições;
  2. converter força kgf → N (×9,81);
  3. plotar subida e descida com barras de erro (dp);
  4. sombrear as regiões definidas na 4.1 (zona morta 96,5–99,5; aderência 99,5–113,5;
     saturação 113,5–117,5) com os nomes;
  5. marcar 116°/117° da descida como pontos ocos (excluídos — corte do ESC).
- **Saída:** `Figuras/curva_forca_comando.png` (200 dpi).
- **Relação com o texto:** evidencia a Tabela-mestra e as regiões; a histerese aparece
  visualmente como laço.

### FIG 4.2 — Corrente de perdas I₀(u) (ensaio em vazio)
- **Fonte:** `ensaios/ensaio_series_vazio.csv` (blocos por degrau, 97→117→97→117).
- **Processamento:**
  1. separar blocos por degrau; descartar execuções com pico < 1 A (comando não executado);
  2. para cada bloco válido: mediana da corrente no platô (50–90% do bloco);
  3. mediana entre as séries → I₀ por degrau; converter θ → u = (θ−95)/85;
  4. ajuste linear (numpy.polyfit ou MATLAB `polyfit`) → I₀ = a + b·u, com r²;
  5. plotar pontos + reta com a equação e o r² na legenda.
- **Saída:** `Figuras/i0_vazio.png`.

### FIG 4.3 — Respostas ao degrau normalizadas + ajuste FOPDT
- **Fonte:** `ensaios/ensaio_cego_subida.csv` (aquisição 100 Hz, timestamps em rajadas).
- **Processamento:**
  1. separar blocos; manter apenas os de degraus 100–109° com >1000 amostras (bordas limpas);
  2. **retempo por índice:** t = k×10 ms (ordem do arquivo preserva a sequência);
  3. normalizar cada resposta pelo platô (mediana dos últimos 5 s): y = I(t)/I_platô;
  4. sobrepor as dez curvas; traçar por cima o ajuste 1 − e^(−t/τ), τ = 1,8 s (linha tracejada);
  5. eixos: tempo 0–6 s, y 0–1,15; legenda com os degraus.
- **Saída:** `Figuras/resposta_degrau.png`.
- **O que a figura prova:** as respostas se sobrepõem após a normalização (o sistema é
  aproximadamente linear em u na região de aderência) e seguem a primeira ordem.

### FIG 4.4 (tabela) — Tabela-mestra e Tabela de incertezas
- Tabela-mestra: mediana ± dp por degrau (feita — valores calculados em 26/10).
- Incertezas: u_A (dp entre escadas), u_B, U(T) por faixa (script separado, mesma fonte).

---

## 2. Da curva à Função de Transferência (a matemática por trás da FIG 4.3)

A FT do caminho comando→corrente é estimada **de cada borda de subida** (degrau de u=0 no
neutro até u_a do degrau). Como o ensaio parte do neutro, a amplitude do degrau é u_a e a
resposta vai de ~0 até I_platô; o ganho de cada borda é K_a = I_platô/u_a. Como a planta é a
mesma para todos os degraus da região de aderência (linearidade — que a FIG 4.3 confirma
pela sobreposição), os parâmetros são **médias entre as dez bordas**:

1. **Ganho estático K:** média dos K_a → esperado 116–125 A/u (cruza com a regressão estática
   de 120 A/u — as duas identificações se validam mutuamente);
2. **Constante de tempo τ — método da 63,2%:** t_63 = instante em que y atinge 0,632;
   τ ≈ t_63 − θ (com θ ≈ 0, τ ≈ t_63);
3. **τ e θ — método dos dois pontos (Ziegler-Nichols):** t_28,3 e t_63,2 →
   τ = 1,5·(t_63,2 − t_28,3); θ = t_63,2 − τ (mais robusto que o ponto único);
4. **Ajuste de mínimos quadrados (MATLAB `lsqcurvefit` ou `tfest`):** minimiza
   Σ[y − K(1−e^(−(t−θ)/τ))]² sobre os três parâmetros — é o que gera os valores que vão ao
   texto (θ ≈ 1,0 s, τ ≈ 1,0 s no LSQ; a soma ≈ 2 s preservada);
5. **Validação cruzada (MATLAB `tfest`):** `tfest` sobre os dados (t, y) com 1 polo + input
   delay retorna a FT diretamente — confrontar com os métodos 2–4; diferenças pequenas =
   robustez.

**Resultado (o que já sabemos dos dados):**
```
G1(s) = K·e^(−θa·s) / (τ·s + 1),   K ≈ 120 A/u,  τ ≈ 1,8–2,0 s,  θa < 0,1 s
```
**Como a FT se relaciona com os gráficos:** a resposta ao degrau da FT (item 3) é, por
definição, a curva tracejada da FIG 4.3 — o gráfico mostra o dado, a FT é o modelo que o
reproduz. O Bode de G1(s) (Cap. 5) sai da mesma FT.

## 3. Como será a resposta ao degrau (esperada e por quê)

Com τ = 1,8 s e θ ≈ 0 (primeira ordem):
- **t = 1,8 s:** 63% do valor final; **t = 3,6 s:** 86%; **t = 5,4 s:** 95%; **t = 7,2 s:** 98%;
- **sem sobressinal** (primeira ordem pura) e **sem atraso visível** na escala do gráfico
  (θ < 0,1 s é 1/18 de τ);
- o MATLAB confirma com `step(G1)` — e no Cap. 5, a mesma chamada gera a resposta em malha
  fechada do PI projetado (PSR) e a rejeição de perturbação (PRP).

Script: `eng.step(sys1, matlab.double(8.0))` → extrair (y, t) → plotar com matplotlib.

---

## 4. Arquitetura dos scripts (pasta `ensaios/figuras/`)

| Script | Entrada | Saída |
|---|---|---|
| `fig_curva.py` | pfc kaka.xlsx | curva_forca_comando.png |
| `fig_i0.py` | ensaio_series_vazio.csv | i0_vazio.png + parâmetros do ajuste |
| `fig_dinamica.py` | ensaio_cego_subida.csv | resposta_degrau.png + K, τ, θ (4 métodos) |
| `identifica_tf.py` | ensaio_cego_subida.csv | G1(s) via MATLAB (tfest + LSQ), salva `g1.mat`/JSON |
| `fig_resposta_mc.py` | G1(s) + ganhos do PI (Cap. 5) | respostas malha fechada (PSR/PRP) |

Cada script: pré-processa em Python → chama o MATLAB só para a caixa-preta → plota em
matplotlib → salva PNG em `PFC_monografia/Figuras/` e imprime os parâmetros no terminal.

## 5. Decisões para a autora
1. **[ ]** Confirmar instalação do `matlab.engine` (comando da Seção 0) — ou autorizar o
   fallback `python-control`;
2. **[ ]** FIG 4.3 usa as dez bordas (100–109°) ou um subconjunto (ex.: 100–105°) para
   legenda menos carregada? Sugestão: todas, legenda em duas colunas;
3. **[ ]** A FT final do texto sai do LSQ (θ~1+τ~1) ou da 63,2% (θ≈0, τ=1,8)? Sugestão:
   reportar a 63,2% como principal (mais estável) e o LSQ como verificação — como já está
   escrito na 4.5;
4. **[ ]** `tfest` exige System Identification Toolbox — verificar licença no R2025b; se não
   houver, os métodos 2–4 bastam e o tfest vira opcional.
