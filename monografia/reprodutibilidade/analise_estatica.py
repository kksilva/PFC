"""Processamento dos dados da caracterizacao estatica.

Le a planilha de anotacoes do ensaio de tracao de corrente versus forca
('ensaio_tracao_corrente_versus_forca.xlsx') e o ensaio
em vazio ('ensaio_vazio_corrente.csv'), ajusta as retas por minimos quadrados,
imprime os coeficientes com o r2 e gera as figuras i0_vazio.png e
curva_forca_comando.png.

Uso:  python3 analise_estatica.py
"""

import csv
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import openpyxl

PASTA_DADOS = Path(__file__).resolve().parent
PASTA_FIGURAS = Path(__file__).resolve().parent

G = 9.80665            # conversao de kgf para N
ANGULO_NEUTRO = 95.0   # comando neutro do ESC (graus)
FAIXA_COMANDO = 85.0   # 95 a 180 graus -> u de 0 a 1
RAIO_EFETIVO_M = 0.0751


def u_de(angulo):
    """Comando normalizado u = (angulo - neutro) / faixa."""
    return (angulo - ANGULO_NEUTRO) / FAIXA_COMANDO


def minimos_quadrados(x, y):
    """Reta y = a + b x por minimos quadrados. Devolve (a, b, r2)."""
    xm = statistics.mean(x)
    ym = statistics.mean(y)
    b = sum((xi - xm) * (yi - ym) for xi, yi in zip(x, y)) / sum((xi - xm) ** 2 for xi in x)
    a = ym - b * xm
    r2 = 1 - sum((yi - a - b * xi) ** 2 for xi, yi in zip(x, y)) / sum((yi - ym) ** 2 for yi in y)
    return a, b, r2


def minimos_quadrados_origem(x, y):
    """Reta y = g x forcada pela origem. Devolve (g, r2)."""
    g = sum(xi * yi for xi, yi in zip(x, y)) / sum(xi * xi for xi in x)
    ym = statistics.mean(y)
    r2 = 1 - sum((yi - g * xi) ** 2 for xi, yi in zip(x, y)) / sum((yi - ym) ** 2 for yi in y)
    return g, r2


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
    pagina = planilha.worksheets[0]
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


def mediana(valores):
    return statistics.median(valores)


def ajuste_gf(pares, degraus, i0_a, i0_b):
    """G_F da reta F = G_F (I - I0(u))/u sobre os pares dos degraus dados."""
    x, y = [], []
    for degrau in degraus:
        u = u_de(degrau)
        for corrente, forca in pares[degrau]:
            x.append((corrente - (i0_a + i0_b * u)) / u)
            y.append(forca)
    return minimos_quadrados_origem(x, y) + (len(x),)


def main():
    # 1) Corrente de perdas I0(u), ajuste sobre as medias por degrau do vazio
    vazio = carregar_vazio()
    x = [u_de(a) for a in sorted(vazio)]
    y = [vazio[a] for a in sorted(vazio)]
    a0, b0, r2_0 = minimos_quadrados(x, y)
    print(f"I0(u) = {a0:.4f} + {b0:.4f} u   r2 = {r2_0:.4f}   n = {len(x)}")

    def i0(u):
        return a0 + b0 * u

    # 2) Curva caracteristica F = G_F (I - I0(u))/u, por sentido
    tracao = carregar_tracao()
    gf_d, r2_d, n_d = ajuste_gf(tracao["DESCIDA"], range(100, 114), a0, b0)
    gf_s, r2_s, n_s = ajuste_gf(tracao["SUBIDA"], range(100, 111), a0, b0)
    print(f"descida: G_F = {gf_d:.4f} N/(A/u)   r2 = {r2_d:.4f}   n = {n_d}")
    print(f"subida : G_F = {gf_s:.4f} N/(A/u)   r2 = {r2_s:.4f}   n = {n_s}")
    print(f"K_T = G_F * r_ef = {gf_d * RAIO_EFETIVO_M:.4f} N*m/(A/u)")

    # 3) Medianas por degrau (conferencia com a tabela da monografia)
    for sentido in ("SUBIDA", "DESCIDA"):
        print(f"--- {sentido} ---")
        for degrau in sorted(tracao[sentido]):
            pares = tracao[sentido][degrau]
            if not pares:
                continue
            correntes = [p[0] for p in pares]
            forcas = [p[1] for p in pares]
            dp = statistics.stdev(correntes) if len(correntes) > 1 else 0.0
            dpf = statistics.stdev(forcas) if len(forcas) > 1 else 0.0
            print(f"{degrau:>3} gr  I = {mediana(correntes):5.2f} +/- {dp:.2f} A   "
                  f"F = {mediana(forcas):5.2f} +/- {dpf:.2f} N")

    # 3b) Tabela do ensaio em vazio (medias por degrau, para a monografia)
    print("--- VAZIO: medias por degrau ---")
    for angulo in sorted(vazio):
        print(f"{int(angulo)} gr  u = {u_de(angulo):.3f}   I0 = {vazio[angulo]:.2f} A")

    # 4) Figuras
    plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": 0.3,
                         "axes.axisbelow": True})

    fig, eixo = plt.subplots(figsize=(6.4, 4.2))
    eixo.axvspan(0.0, u_de(99.5), color="0.9")
    eixo.text(u_de(98), 2.45, "zona morta", ha="center", fontsize=8)
    eixo.plot(x, y, "o", color="#2166ac", ms=4.5,
              label="Media por degrau (ensaio em vazio)")
    u_lin = [0.0, max(x)]
    eixo.plot(u_lin, [a0 + b0 * u for u in u_lin], "-", color="#b2182b",
              label=f"$I_0 = {a0:.2f} + {b0:.2f}\\,u$  ($r^2 = {r2_0:.2f}$)")
    eixo.set_xlabel("Comando normalizado $u$  ($u = (\\alpha - 95)/85$)")
    eixo.set_ylabel("Corrente de perdas $I_0$ (A)")
    eixo.set_ylim(0, 2.7)
    eixo.legend(fontsize=9, loc="upper left")
    fig.tight_layout()
    fig.savefig(PASTA_FIGURAS / "i0_vazio.png", dpi=200)
    plt.close(fig)

    fig, eixo = plt.subplots(figsize=(6.8, 4.4))
    cores = {"SUBIDA": "#d6604d", "DESCIDA": "#2166ac"}
    marcadores = {"SUBIDA": "s", "DESCIDA": "o"}
    for sentido in ("SUBIDA", "DESCIDA"):
        degs = [a for a in sorted(tracao[sentido]) if tracao[sentido][a]]
        fs = [mediana([p[1] for p in tracao[sentido][a]]) for a in degs]
        eixo.plot(degs, fs, marcadores[sentido], ms=5, color=cores[sentido],
                  mec=cores[sentido], lw=1, label=sentido.capitalize())
        if sentido == "DESCIDA":
            # pontos do corte do ESC ficam ocos, fora da curva
            degs_corte = [a for a in degs if a >= 116]
            fs_corte = [mediana([p[1] for p in tracao[sentido][a]]) for a in degs_corte]
            eixo.plot(degs_corte, fs_corte, "o", ms=7, mfc="none",
                      mec=cores[sentido], lw=1.2)
    eixo.axvspan(96.5, 99.5, color="0.9")
    eixo.axvspan(99.5, 113.5, color="0.96")
    eixo.text(98, 55, "zona morta", ha="center", fontsize=8)
    eixo.text(106, 55, "aderencia", ha="center", fontsize=8)
    eixo.text(115.5, 55, "saturacao", ha="center", fontsize=8)
    eixo.set_xlabel("Degrau de comando (graus)")
    eixo.set_ylabel("Forca de tracao (N)")
    eixo.set_ylim(0, 60)
    eixo.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(PASTA_FIGURAS / "curva_forca_comando.png", dpi=200)
    plt.close(fig)
    print(f"figuras salvas em {PASTA_FIGURAS}")


if __name__ == "__main__":
    main()
