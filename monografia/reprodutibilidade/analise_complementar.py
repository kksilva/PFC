"""Analises complementares da caracterizacao estatica (figuras de apoio).

Le a planilha de anotacoes do ensaio de tracao de corrente versus forca
('ensaio_tracao_corrente_versus_forca.xlsx', 4 repeticoes por sentido) e o
ensaio em vazio ('ensaio_vazio_corrente.csv') e gera tres figuras para a
pasta PFC_monografia/Figuras (300 dpi):

1. corrente_comando.png  - corrente mediana por degrau, subida e descida,
   com barras de erro do desvio-padrao das repeticoes e as regioes de
   operacao (zona morta / aderencia / saturacao) sombreadas;
2. forca_fase_scatter.png - forca versus corrente de fase equivalente
   (I - I0(u))/u para cada ponto individual das repeticoes, com as retas
   ajustadas F = G_F (I - I0)/u por sentido (figura central de validacao
   do modelo de torque);
3. forca_boxplot.png - dispersao da forca por degrau na regiao de
   aderencia (boxplot + pontos das repeticoes), evidenciando o plato da
   subida frente ao crescimento da descida.

Uso:  python3 analise_complementar.py
"""

# ---------------------------------------------------------------------------
# MAPA
# 1) Constantes do projeto (linhas 45-49)
# 2) Funcoes auxiliares: leitura da planilha e do vazio, minimos quadrados
#    pela origem (linhas 52-105)
# 3) Figura corrente_comando.png (linhas 108-145)
# 4) Figura forca_fase_scatter.png (linhas 148-195)
# 5) Figura forca_boxplot.png (linhas 198-235)
# ---------------------------------------------------------------------------

import csv
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import openpyxl

PASTA_DADOS = Path(__file__).resolve().parent
PASTA_FIGURAS = PASTA_DADOS.parent / "Figuras"

G = 9.81               # conversao de kgf para N (mesmo valor da monografia)
ANGULO_NEUTRO = 95.0   # comando neutro do ESC (graus)
FAIXA_COMANDO = 85.0   # 95 a 180 graus -> u de 0 a 1

DEGRAUS_SUBIDA = range(100, 111)   # faixa de aderencia validada (subida)
DEGRAUS_DESCIDA = range(100, 114)  # faixa de aderencia validada (descida)


def u_de(angulo):
    """Comando normalizado u = (angulo - neutro) / faixa."""
    return (angulo - ANGULO_NEUTRO) / FAIXA_COMANDO


def carregar_vazio():
    """Medias da corrente de perdas por degrau, do ensaio em vazio."""
    por_angulo = {}
    with open(PASTA_DADOS / "ensaio_vazio_corrente.csv") as arquivo:
        for linha in csv.DictReader(arquivo, delimiter=";"):
            por_angulo.setdefault(float(linha["angulo"]), []).append(float(linha["corrente_a"]))
    return {a: sum(v) / len(v) for a, v in por_angulo.items()}


def carregar_tracao():
    """Pares (corrente_A, forca_N) por sentido e por degrau, das 4 repeticoes."""
    planilha = openpyxl.load_workbook(PASTA_DADOS / "ensaio_tracao_corrente_versus_forca.xlsx", data_only=True)
    pagina = planilha["Página1"]
    degraus = [int(pagina.cell(row=1, column=c).value) for c in range(2, 44, 2)]
    tracao = {"SUBIDA": {a: [] for a in degraus}, "DESCIDA": {a: [] for a in degraus}}
    for linha in pagina.iter_rows(min_row=3, values_only=True):
        if linha[0] not in tracao:
            continue
        for j, degrau in enumerate(degraus):
            corrente, forca = linha[1 + 2 * j], linha[2 + 2 * j]
            if corrente is not None and forca is not None:
                tracao[linha[0]][degrau].append((float(corrente), float(forca) * G))
    return tracao


def ajuste_origem(x, y):
    """Reta y = g x forcada pela origem. Devolve (g, r2)."""
    g = sum(xi * yi for xi, yi in zip(x, y)) / sum(xi * xi for xi in x)
    ym = statistics.mean(y)
    r2 = 1 - sum((yi - g * xi) ** 2 for xi, yi in zip(x, y)) / sum((yi - ym) ** 2 for yi in y)
    return g, r2


def i0_ajustado(vazio):
    """I0(u) = a + b u por minimos quadrados sobre as medias do ensaio em vazio."""
    xs = [u_de(a) for a in sorted(vazio)]
    ys = [vazio[a] for a in sorted(vazio)]
    xm, ym = statistics.mean(xs), statistics.mean(ys)
    b = sum((xi - xm) * (yi - ym) for xi, yi in zip(xs, ys)) / sum((xi - xm) ** 2 for xi in xs)
    return ym - b * xm, b


def main():
    vazio = carregar_vazio()
    a0, b0 = i0_ajustado(vazio)
    tracao = carregar_tracao()
    cores = {"SUBIDA": "#d6604d", "DESCIDA": "#2166ac"}
    marcadores = {"SUBIDA": "s", "DESCIDA": "o"}
    rotulos = {"SUBIDA": "Subida", "DESCIDA": "Descida"}
    faixas = [range(97, 100), DEGRAUS_SUBIDA, range(111, 118)]
    nomes_faixas = ["zona morta", "aderencia", "saturacao"]

    plt.rcParams.update({"font.size": 11.5, "axes.grid": True, "grid.alpha": 0.3,
                         "axes.axisbelow": True, "axes.titlesize": 13})

    # ------------------------------------------------------------------
    # 1) corrente_comando.png: mediana +- desvio-padrao por degrau
    # ------------------------------------------------------------------
    fig, eixo = plt.subplots(figsize=(7.0, 4.6))
    for faixa, nome in zip(faixas, nomes_faixas):
        x0 = min(faixa) - 0.5
        x1 = max(faixa) + 0.5
        eixo.axvspan(x0, x1, color="0.9" if nome != "aderencia" else "0.96")
        eixo.text((x0 + x1) / 2, 31.5, nome, ha="center", fontsize=10)
    for sentido in ("SUBIDA", "DESCIDA"):
        degs = [a for a in sorted(tracao[sentido]) if tracao[sentido][a]]
        meds = [statistics.median([p[0] for p in tracao[sentido][a]]) for a in degs]
        dps = [statistics.stdev([p[0] for p in tracao[sentido][a]]) if len(tracao[sentido][a]) > 1
               else 0.0 for a in degs]
        eixo.errorbar(degs, meds, yerr=dps, fmt=marcadores[sentido], ms=6,
                      color=cores[sentido], ecolor=cores[sentido], elinewidth=1.2,
                      capsize=3, label=f"{rotulos[sentido]} (mediana +- desvio-padrao, 4 repeticoes)")
    eixo.set_title("Corrente de armadura mediana por degrau de comando")
    eixo.set_xlabel("Degrau de comando (graus)")
    eixo.set_ylabel("Corrente (A)")
    eixo.set_ylim(0, 34)
    eixo.legend(fontsize=10, loc="center right")
    fig.tight_layout()
    fig.savefig(PASTA_FIGURAS / "corrente_comando.png", dpi=300)
    plt.close(fig)

    # ------------------------------------------------------------------
    # 2) forca_fase_scatter.png: validacao do modelo F = G_F (I - I0)/u
    # ------------------------------------------------------------------
    fig, eixo = plt.subplots(figsize=(6.8, 4.8))
    ganhos = {}
    for sentido, degs in (("DESCIDA", DEGRAUS_DESCIDA), ("SUBIDA", DEGRAUS_SUBIDA)):
        xs, ys = [], []
        for degrau in degs:
            u = u_de(degrau)
            for corrente, forca in tracao[sentido][degrau]:
                xs.append((corrente - (a0 + b0 * u)) / u)
                ys.append(forca)
        g, r2 = ajuste_origem(xs, ys)
        ganhos[sentido] = (g, r2, len(xs))
        eixo.plot(xs, ys, marcadores[sentido], ms=5.5, color=cores[sentido],
                  alpha=0.75, mec="white", mew=0.4,
                  label=f"{rotulos[sentido]}: {len(xs)} pontos (4 repeticoes)")
        x_lin = [0.0, max(xs) * 1.05]
        eixo.plot(x_lin, [g * x for x in x_lin], "-", color=cores[sentido], lw=1.8,
                  label=f"$G_F$ {rotulos[sentido].lower()} = {g:.3f} N/(A/u)  ($r^2 = {r2:.3f}$)")
        print(f"{sentido.lower()}: G_F = {g:.4f} N/(A/u)   r2 = {r2:.4f}   n = {len(xs)}")
    eixo.set_title("Validacao do modelo: forca versus corrente de fase equivalente")
    eixo.set_xlabel("Corrente de fase equivalente  $(I - I_0(u))/u$  (A)")
    eixo.set_ylabel("Forca de tracao (N)")
    eixo.legend(fontsize=10, loc="upper left")
    fig.tight_layout()
    fig.savefig(PASTA_FIGURAS / "forca_fase_scatter.png", dpi=300)
    plt.close(fig)

    # ------------------------------------------------------------------
    # 3) forca_boxplot.png: dispersao por degrau na regiao de aderencia
    # ------------------------------------------------------------------
    degs = list(DEGRAUS_SUBIDA)
    fig, eixo = plt.subplots(figsize=(8.2, 4.6))
    largura = 0.36
    for k, sentido in enumerate(("SUBIDA", "DESCIDA")):
        posicoes = [d + (k - 0.5) * largura for d in degs]
        dados = [[p[1] for p in tracao[sentido][d]] for d in degs]
        caixas = eixo.boxplot(dados, positions=posicoes, widths=largura * 0.9,
                              patch_artist=True, manage_ticks=False,
                              medianprops=dict(color="black", lw=1.4),
                              boxprops=dict(facecolor=cores[sentido], alpha=0.45,
                                            edgecolor=cores[sentido]),
                              whiskerprops=dict(color=cores[sentido]),
                              capprops=dict(color=cores[sentido]),
                              flierprops=dict(marker=""))
        # pontos individuais das repeticoes, com leve deslocamento horizontal
        for p, d in zip(posicoes, degs):
            for rep, (corrente, forca) in enumerate(tracao[sentido][d]):
                eixo.plot(p + (rep - 1.5) * 0.03, forca, marcadores[sentido],
                          ms=4, color=cores[sentido], mec="white", mew=0.3)
        eixo.plot([], [], marcadores[sentido], color=cores[sentido], ms=6,
                  label=f"{rotulos[sentido]} (4 repeticoes)")
    eixo.axvspan(99.5, 110.5, color="0.96", zorder=0)
    eixo.text(105, 55.5, "regiao de aderencia (validada)", ha="center", fontsize=10)
    eixo.set_title("Dispersao da forca por degrau na regiao de aderencia")
    eixo.set_xlabel("Degrau de comando (graus)")
    eixo.set_ylabel("Forca de tracao (N)")
    eixo.set_xticks(degs)
    eixo.set_ylim(0, 60)
    eixo.legend(fontsize=10.5, loc="lower right")
    fig.tight_layout()
    fig.savefig(PASTA_FIGURAS / "forca_boxplot.png", dpi=300)
    plt.close(fig)

    print(f"figuras salvas em {PASTA_FIGURAS}")


if __name__ == "__main__":
    main()
