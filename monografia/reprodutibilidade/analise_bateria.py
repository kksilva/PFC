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
- Figuras/bateria_sag.png (300 dpi): mediana de corrente por degrau das duas
  sessoes, com o ponto colapsado das retomadas do degrau de 114 graus da
  sessao degradada destacado e anotado.

Uso:  python3 analise_bateria.py
"""

# ---------------------------------------------------------------------------
# MAPA
# 1) Constantes e leitura dos CSVs (linhas 46-66)
# 2) Separacao dos blocos de degrau e estatisticas por bloco (linhas 69-96)
# 3) Selecao das corridas: boa (subida principal) e antiga (descida) (linhas 99-124)
# 4) Deteccao dos ciclos de corte do ESC no bloco colapsado (linhas 127-144)
# 5) Figura bateria_sag.png e numeros-chave impressos (linhas 147-178)
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
        "font.size": 11, "axes.grid": True, "grid.alpha": 0.3,
        "font.family": "serif", "axes.titlesize": 12,
    })

    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    fig.suptitle("Mediana da corrente por degrau: bateria em bom estado vs bateria degradada",
                 fontsize=13)
    ax.plot([b["angulo"] for b in boa], [b["mediana"] for b in boa],
            "-", color="tab:blue", lw=2, label="Bateria boa (subida)")
    ax.plot([b["angulo"] for b in ant_saudavel], [b["mediana"] for b in ant_saudavel],
            "-", color="tab:orange", lw=2, label="Bateria antiga (descida, 1.a passagem)")
    ax.plot(ant_colapso["angulo"], ant_colapso["mediana"], "v", color="tab:red",
            markersize=10, label="Bateria antiga (retomadas, colapso)")
    ax.annotate(f"{ant_colapso['mediana']:.0f} A ({100*ant_colapso['frac_zero']:.0f} % em zero)",
                xy=(ant_colapso["angulo"], ant_colapso["mediana"]),
                xytext=(ant_colapso["angulo"] - 3, ant_colapso["mediana"] - 6),
                fontsize=10, ha="right", arrowprops=dict(arrowstyle="->", lw=0.9))
    ax.set_xlabel("Degrau de comando (graus)")
    ax.set_ylabel("Mediana da corrente (A)")
    ax.set_ylim(0, 33)
    ax.legend(fontsize=10.5, loc="upper left")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(PASTA_FIGURAS / "bateria_sag.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"\nFigura salva em {PASTA_FIGURAS / 'bateria_sag.png'}")


if __name__ == "__main__":
    main()
