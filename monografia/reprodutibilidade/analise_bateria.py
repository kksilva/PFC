"""Analise do efeito de bateria degradada (sag de tensao e corte do ESC).

Durante os ensaios de degraus de comando, uma das sessoes de descida foi
executada com baterias antigas/degradadas do laboratorio. Sob alta corrente,
a tensao da bateria caia (sag severo) e o corte de subtensao do ESC
interrompia o motor, gerando um comportamento ciclico de aceleracao e parada.
Esta rotina compara essa sessao com a sessao de referencia (bateria boa,
ensaio de subida) e gera a figura 'bateria_sag.png' para a monografia.

LE:
- ensaios/ensaio_cego_descida.csv (sessao com bateria antiga; colunas
  t_ensaio_s, t_degrau_s, angulo, corrente_a, amostragem ~100 Hz)
- reprodutibilidade/ensaio_tracao_corrente.csv (sessao de referencia com
  bateria boa, mesmo formato; usa a corrida principal de 100 a 114 graus)

GERA:
- Figuras/bateria_sag.png (300 dpi): painel (a) com a mediana de corrente
  por degrau das duas sessoes, evidenciando o colapso nas retomadas do
  degrau de 114 graus da sessao degradada; painel (b) com a forma de onda
  a 100 Hz do degrau colapsado ao lado do degrau saudavel de referencia.

Uso:  python3 analise_bateria.py
"""

# ---------------------------------------------------------------------------
# MAPA
# 1) Constantes e leitura dos CSVs (linhas 40-60)
# 2) Separacao dos blocos de degrau e estatisticas por bloco (linhas 63-90)
# 3) Selecao das corridas: boa (subida principal) e antiga (descida) (linhas 93-120)
# 4) Deteccao dos ciclos de corte do ESC no bloco colapsado (linhas 123-140)
# 5) Figura bateria_sag.png (linhas 143-210)
# 6) Impressao dos numeros-chave para o texto da monografia (linhas 213-245)
# ---------------------------------------------------------------------------

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PASTA_RAIZ = Path(__file__).resolve().parents[2]
PASTA_DADOS = PASTA_RAIZ / "ensaios"
PASTA_REPRO = Path(__file__).resolve().parent
PASTA_FIGURAS = PASTA_REPRO.parent / "Figuras"

TAXA_HZ = 100.0          # amostragem da corrente nos ensaios (~1500 amostras/15 s)
LIMIAR_CORTE_A = 5.0     # abaixo disso o motor esta cortado (corrente de repouso ~0 A)
TAXA_REF = PASTA_REPRO / "ensaio_tracao_corrente.csv"
TAXA_ANTIGA = PASTA_DADOS / "ensaio_cego_descida.csv"


def ler_csv(caminho):
    """Le o CSV do ensaio (separador ';') e retorna matriz [t_ensaio, t_degrau, angulo, corrente]."""
    with open(caminho) as arquivo:
        linhas = list(csv.reader(arquivo, delimiter=";"))
    return np.array([[float(v) for v in linha] for linha in linhas[1:] if len(linha) == 4])


def separar_blocos(dados):
    """Separa a serie em blocos contiguos de mesmo angulo de comando."""
    angulos = dados[:, 2]
    blocos = []
    inicio = 0
    for i in range(1, len(dados) + 1):
        if i == len(dados) or angulos[i] != angulos[inicio]:
            blocos.append(dados[inicio:i])
            inicio = i
    return blocos


def estatistica_bloco(bloco):
    """Mediana, percentil 95 e fracao de amostras abaixo de 0,5 A de um bloco."""
    corrente = bloco[:, 3]
    return {
        "angulo": bloco[0, 2],
        "n": len(bloco),
        "mediana": float(np.median(corrente)),
        "p95": float(np.percentile(corrente, 95)),
        "frac_zero": float((np.abs(corrente) < 0.5).mean()),
        "t_degrau": bloco[:, 1],
        "corrente": corrente,
    }


def main():
    # --- 1) leitura -------------------------------------------------------
    referencia = ler_csv(TAXA_REF)
    antiga = ler_csv(TAXA_ANTIGA)

    blocos_ref = [estatistica_bloco(b) for b in separar_blocos(referencia)]
    blocos_ant = [estatistica_bloco(b) for b in separar_blocos(antiga)]

    # --- 2) selecao das corridas ------------------------------------------
    # Referencia (bateria boa): corrida principal da subida, blocos de ~15 s
    # (~1500 amostras) de 100 a 114 graus, com corrente crescente normal.
    # Blocos de 1 Hz (n pequeno) e blocos com picos > 100 A (corrompidos,
    # ver ensaio_consolidado.csv) sao descartados.
    boa = [
        b for b in blocos_ref
        if 100 <= b["angulo"] <= 114 and b["n"] > 1000 and b["p95"] < 100
    ]
    boa.sort(key=lambda b: b["angulo"])
    # a corrida principal sobe de 100 a 114 sem repetir angulo; retomadas
    # posteriores do mesmo degrau (ultima corrida do arquivo) sao descartadas
    vistos = set()
    boa = [b for b in boa if not (b["angulo"] in vistos or vistos.add(b["angulo"]))]

    # Sessao com bateria antiga (descida): primeira passagem 120 -> 113,
    # blocos saudaveis de ~15 s; as retomadas do degrau de 114 graus sao o
    # bloco final colapsado (3 tentativas, corrente ciclando ate zerar).
    ant_saudavel = [
        b for b in blocos_ant
        if b["angulo"] >= 113 and b["n"] > 1000 and b["frac_zero"] < 0.3
    ]
    ant_colapso = max(blocos_ant, key=lambda b: b["frac_zero"])

    # --- 3) deteccao dos ciclos de corte no bloco colapsado ---------------
    ligado = ant_colapso["corrente"] > LIMIAR_CORTE_A
    bordas = np.diff(ligado.astype(int))
    religamentos = np.where(bordas == 1)[0]
    desligamentos = np.where(bordas == -1)[0]
    corrente_ligada = ant_colapso["corrente"][ligado]
    mediana_ligada = float(np.median(corrente_ligada)) if len(corrente_ligada) else float("nan")

    # --- 4) numeros-chave --------------------------------------------------
    boa_por_angulo = {b["angulo"]: b for b in boa}
    ref_114 = boa_por_angulo[114.0]
    print("=== Sessao de referencia (bateria boa, subida) - mediana por degrau ===")
    for b in boa:
        print(f"  {b['angulo']:5.0f} graus: mediana = {b['mediana']:5.1f} A "
              f"(p95 = {b['p95']:5.1f} A, zeros = {100*b['frac_zero']:.0f} %)")
    print("\n=== Sessao com bateria antiga (descida) - primeira passagem ===")
    for b in sorted(ant_saudavel, key=lambda b: -b["angulo"]):
        print(f"  {b['angulo']:5.0f} graus: mediana = {b['mediana']:5.1f} A "
              f"(p95 = {b['p95']:5.1f} A, zeros = {100*b['frac_zero']:.0f} %)")
    print("\n=== Colapso nas retomadas do degrau de 114 graus (bateria antiga) ===")
    print(f"  mediana do bloco: {ant_colapso['mediana']:.1f} A "
          f"(vs {ref_114['mediana']:.1f} A no degrau de 114 graus da sessao boa)")
    print(f"  amostras ~zero: {100*ant_colapso['frac_zero']:.0f} %")
    print(f"  corrente com o motor ligado: mediana = {mediana_ligada:.1f} A "
          f"(p95 = {np.percentile(corrente_ligada, 95):.1f} A)")
    print(f"  religamentos do motor detectados: {len(religamentos)} "
          f"(ciclos de corte e retomada do ESC)")

    # --- 5) figura ----------------------------------------------------------
    plt.rcParams.update({
        "font.size": 10, "axes.grid": True, "grid.alpha": 0.3,
        "font.family": "serif",
    })

    fig, eixos = plt.subplots(
        2, 2, figsize=(7.0, 5.6),
        gridspec_kw={"height_ratios": [1.1, 1.0], "hspace": 0.5, "wspace": 0.32},
    )

    # (a) mediana de corrente por degrau
    ax = eixos[0, 0]
    ax.plot([b["angulo"] for b in boa], [b["mediana"] for b in boa],
            "o-", color="tab:blue", label="Bateria boa (subida)")
    ax.plot([b["angulo"] for b in ant_saudavel], [b["mediana"] for b in ant_saudavel],
            "s-", color="tab:orange", label="Bateria antiga (descida, 1.a passagem)")
    ax.plot(ant_colapso["angulo"], ant_colapso["mediana"], "v", color="tab:red",
            markersize=9, label="Bateria antiga (retomadas, colapso)")
    ax.annotate(f"{ant_colapso['mediana']:.0f} A ({100*ant_colapso['frac_zero']:.0f} % zero)",
                xy=(ant_colapso["angulo"], ant_colapso["mediana"]),
                xytext=(ant_colapso["angulo"] + 2, ant_colapso["mediana"] - 4),
                fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.set_xlabel("Degrau de comando (graus)")
    ax.set_ylabel("Mediana da corrente (A)")
    ax.set_title("(a) Corrente por degrau", fontsize=10)
    ax.set_ylim(0, 33)
    rotulos, ident = ax.get_legend_handles_labels()

    # (b) forma de onda do degrau colapsado (100 Hz)
    ax = eixos[0, 1]
    t = ant_colapso["t_degrau"]
    i = np.arange(len(t)) / TAXA_HZ          # tempo dentro do bloco (3 retomadas)
    ax.plot(i, ant_colapso["corrente"], color="tab:red", lw=0.6)
    for k in range(1, 3):                     # separacao visual das 3 tentativas
        ax.axvline(15 * k, color="k", ls="--", lw=0.8)
    for k, centro in enumerate((7.5, 22.5, 37.5)):
        ax.text(centro, 35, f"retomada {k + 1}", fontsize=7.5, ha="center")
    ax.set_xlabel("Tempo no bloco (s)")
    ax.set_ylabel("Corrente (A)")
    ax.set_title("(b) Bateria antiga, degrau de 114 gr: ciclos de corte", fontsize=9)
    ax.set_ylim(-2, 38)

    # (c) forma de onda saudavel de referencia (subida, 113 graus)
    ax = eixos[1, 0]
    ref_113 = boa_por_angulo[113.0]
    ax.plot(ref_113["t_degrau"], ref_113["corrente"], color="tab:blue", lw=0.6)
    ax.set_xlabel("Tempo no degrau (s)")
    ax.set_ylabel("Corrente (A)")
    ax.set_title(f"(c) Bateria boa, degrau de 113 gr\nplato estavel (~{ref_113['mediana']:.0f} A)",
                 fontsize=9)
    ax.set_ylim(-2, 38)

    # (d) detalhe de um ciclo de corte (zoom na primeira retomada)
    ax = eixos[1, 1]
    mascara = i <= 16
    ax.plot(i[mascara], ant_colapso["corrente"][mascara], color="tab:red", lw=0.8)
    ax.axhline(LIMIAR_CORTE_A, color="k", ls=":", lw=0.8)
    ax.text(10.2, 7.5, "corte do ESC (subtensao)", fontsize=7.5)
    ax.set_xlabel("Tempo no bloco (s)")
    ax.set_ylabel("Corrente (A)")
    ax.set_title("(d) Bateria antiga: ligado ->\ncorte -> religamento", fontsize=9)
    ax.set_ylim(-2, 38)

    fig.align_ylabels(eixos)
    fig.legend(rotulos, ident, loc="lower center", ncol=3, fontsize=7.5,
               frameon=False, bbox_to_anchor=(0.5, -0.02))
    fig.savefig(PASTA_FIGURAS / "bateria_sag.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"\nFigura salva em {PASTA_FIGURAS / 'bateria_sag.png'}")


if __name__ == "__main__":
    main()
