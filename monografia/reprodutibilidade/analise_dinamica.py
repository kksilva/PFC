"""Identificacao da dinamica entre comando e corrente (ensaio de tracao de
corrente).

Le 'ensaio_tracao_corrente.csv', isola a sessao de aquisicao rapida (100 Hz),
ancora cada degrau da regiao de aderencia (100 a 109 graus) no seu inicio
eletrico, normaliza as respostas, ajusta a constante de tempo por minimos
quadrados sobre a media das dez bordas e gera as figuras blocos_degrau.png
e resposta_degrau.png.

Uso:  python3 analise_dinamica.py
"""

# ---------------------------------------------------------------------------
# MAPA
# 1) Constantes do projeto: normalizacao do comando, faixa de degraus da identificacao, taxa de amostragem (linhas 36-39)
# 2) Leitura do CSV: segmento 100 Hz, quebra em blocos por degrau (linhas 46-70)
# 3) Ancoragem eletrica de cada borda: repouso, plato e inicio eletrico, mais a resposta normalizada (linhas 72-90)
# 4) Ajuste da constante de tempo tau (funcoes e bloco em main) (linhas 92-119)
# 5) main: ganhos de plato de cada borda e ganho medio (linhas 121-127)
# 6) Figuras: blocos_degrau.png (janelas brutas), blocos_degrau_<angulo>.png (janelas diversificadas) e resposta_degrau.png (linhas 130-192)
# ---------------------------------------------------------------------------

import csv
import math
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

PASTA_DADOS = Path(__file__).resolve().parent
PASTA_FIGURAS = Path(__file__).resolve().parent

ANGULO_NEUTRO = 95.0
FAIXA_COMANDO = 85.0
DEGRAU_MINIMO, DEGRAU_MAXIMO = 100, 109   # bordas usadas na identificacao
AMOSTRAS_POR_SEGUNDO = 100


def u_de(angulo):
    return (angulo - ANGULO_NEUTRO) / FAIXA_COMANDO


def carregar_sessao_rapida():
    """Segmento 100 Hz do CSV: o mais longo, com um bloco por degrau."""
    # O CSV concatena varias sessoes de aquisicao; o timestamp que reseta marca
    # a fronteira entre elas. A sessao mais longa e a de 100 Hz, e nela cada
    # trecho de comando constante vira um bloco (um degrau).
    leituras = []
    with open(PASTA_DADOS / "ensaio_tracao_corrente.csv") as arquivo:
        for linha in csv.DictReader(arquivo, delimiter=";"):
            leituras.append((float(linha["t_ensaio_s"]),
                             float(linha["angulo"]),
                             float(linha["corrente_a"])))
    reseta = [0] + [i for i in range(1, len(leituras))
                    if leituras[i][0] < leituras[i - 1][0]] + [len(leituras)]
    segmentos = [leituras[reseta[k]:reseta[k + 1]] for k in range(len(reseta) - 1)]
    sessao = max(segmentos, key=len)
    blocos = []
    bloco = [sessao[0]]
    for leitura in sessao[1:]:
        if leitura[1] != bloco[-1][1]:
            blocos.append(bloco)
            bloco = []
        bloco.append(leitura)
    blocos.append(bloco)
    return blocos


def iniciar_em(bloco):
    """Ancora o bloco no inicio eletrico: primeira amostra acima de 20% da excursao."""
    # O inicio eletrico (quando a corrente comeca a subir) nao coincide com o
    # inicio da janela de comando; ancorar na primeira amostra acima de 20% da
    # excursao repouso->plato alinha as dez bordas para a media e o ajuste.
    correntes = [leitura[2] for leitura in bloco]
    repouso = statistics.mean(correntes[:150])       # 1,5 s iniciais (neutro)
    plato = statistics.mean(correntes[-300:])        # 3 s finais (regime)
    alvo = repouso + 0.2 * (plato - repouso)
    inicio = next(i for i, c in enumerate(correntes) if c > alvo)
    return correntes, repouso, plato, inicio


def resposta_normalizada(bloco):
    """Trecho de 6 s a partir do inicio eletrico, normalizado entre 0 e 1."""
    correntes, repouso, plato, inicio = iniciar_em(bloco)
    trecho = correntes[inicio:inicio + 6 * AMOSTRAS_POR_SEGUNDO]
    return [(c - repouso) / (plato - repouso) for c in trecho], repouso, plato


def ajustar_tau(media):
    """Minimiza a soma dos quadrados dos residuos de y = 1 - exp(-t/tau)."""
    # Ajuste direto da resposta de primeira ordem sobre a media das dez bordas,
    # por varredura de tau; serve de contraste ao metodo grafico de 63,2%.
    def residuo(tau):
        return sum((y - (1 - math.exp(-i / AMOSTRAS_POR_SEGUNDO / tau))) ** 2
                   for i, y in enumerate(media))
    return min(range(5, 1000, 5), key=lambda t: residuo(t / 1000)) / 1000


def media_movel(serie, janela):
    return [statistics.mean(serie[max(0, i - janela + 1):i + 1])
            for i in range(len(serie))]


def main():
    blocos = carregar_sessao_rapida()
    usados = [b for b in blocos if DEGRAU_MINIMO <= b[0][1] <= DEGRAU_MAXIMO]
    assert len(usados) == 10  # dez bordas 100-109: usados[0/3/6/9] dependem disso
    print(f"bordas usadas: {[int(b[0][1]) for b in usados]}")

    # constante de tempo sobre a media das respostas normalizadas
    respostas = [resposta_normalizada(b) for b in usados]
    normais = [r[0] for r in respostas]
    n = min(len(r) for r in normais)
    media = [statistics.mean(r[i] for r in normais) for i in range(n)]
    tau = ajustar_tau(media)
    tau_632 = next(i for i, v in enumerate(media) if v >= 0.632) / AMOSTRAS_POR_SEGUNDO
    print(f"tau (minimos quadrados) = {tau:.2f} s | tau (63,2%) = {tau_632:.2f} s")

    # ganho de cada borda: plato por unidade de comando
    ganhos = []
    for bloco, (normalizada, repouso, plato) in zip(usados, respostas):
        angulo = int(bloco[0][1])
        ganho = plato / u_de(angulo)
        ganhos.append(ganho)
        print(f"{angulo} gr: plato = {plato:.2f} A | ganho = {ganho:.0f} A/u")
    print(f"ganho medio das dez bordas = {statistics.mean(ganhos):.1f} A/u")

    # figura 1: janelas brutas de dois degraus, com media movel
    plt.rcParams.update({"font.size": 11, "axes.grid": True, "grid.alpha": 0.3,
                         "axes.axisbelow": True, "axes.titlesize": 12})
    fig, eixos = plt.subplots(1, 2, figsize=(9.4, 3.8), sharey=True)
    for eixo, bloco in zip(eixos, (usados[0], usados[6])):
        correntes, _, _, _ = iniciar_em(bloco)
        tempo = [i / AMOSTRAS_POR_SEGUNDO for i in range(len(correntes))]
        eixo.plot(tempo, correntes, color="0.75", lw=0.8, label="Corrente bruta (100 Hz)")
        eixo.plot(tempo, media_movel(correntes, 50), color="#b2182b", lw=1.6,
                  label="Media movel (0,5 s)")
        eixo.set_xlabel("Tempo desde o inicio da janela (s)")
        eixo.set_title(f"Degrau de comando {int(bloco[0][1])} gr", fontsize=12)
        eixo.set_xlim(0, 8)
    eixos[0].set_ylabel("Corrente (A)")
    eixos[0].legend(fontsize=10)
    fig.suptitle("Janelas brutas de corrente nos degraus de comando (ensaio a 100 Hz)",
                 fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(PASTA_FIGURAS / "blocos_degrau.png", dpi=300)
    plt.close(fig)

    # figura 2: respostas alinhadas, media e ajuste de primeira ordem
    fig, eixo = plt.subplots(figsize=(6.4, 4.4))
    tempo = [i / AMOSTRAS_POR_SEGUNDO for i in range(n)]
    for normalizada, _, _ in respostas:
        eixo.plot(tempo[:len(normalizada)], normalizada, color="0.8", lw=0.9)
    eixo.plot(tempo, media, color="#2166ac", lw=2.0, label="Media das dez bordas")
    ajuste = [1 - math.exp(-t / tau) for t in tempo]
    eixo.plot(tempo, ajuste, "--", color="#b2182b", lw=1.8,
              label=f"Ajuste de 1.a ordem: $1-e^{{-t/{tau:.2f}}}$")
    eixo.plot(tau, 1 - math.exp(-1), "o", color="#b2182b")
    eixo.annotate("$\\tau$", (tau, 0.632), textcoords="offset points",
                  xytext=(8, -4), fontsize=12)
    eixo.set_title("Resposta normalizada das dez bordas: media e ajuste de 1.a ordem")
    eixo.set_xlabel("Tempo desde o inicio eletrico (s)")
    eixo.set_ylabel("Resposta normalizada")
    eixo.set_xlim(0, 2.5)
    eixo.legend(fontsize=10.5)
    fig.tight_layout()
    # figuras 1b e 1c: janela bruta de um degrau no inicio e no fim da regiao
    for indice in (3, 9):
        bloco = usados[indice]
        angulo = int(bloco[0][1])
        correntes, _, _, _ = iniciar_em(bloco)
        tempo = [i / AMOSTRAS_POR_SEGUNDO for i in range(len(correntes))]
        fig, eixo = plt.subplots(figsize=(6.4, 3.6))
        eixo.plot(tempo, correntes, color="0.75", lw=0.8, label="Corrente bruta (100 Hz)")
        eixo.plot(tempo, media_movel(correntes, 50), color="#b2182b", lw=1.6,
                  label="Media movel (0,5 s)")
        eixo.set_xlabel("Tempo desde o inicio da janela (s)")
        eixo.set_ylabel("Corrente (A)")
        eixo.set_xlim(0, 8)
        eixo.set_title(f"Janela bruta do degrau de comando {angulo} graus (ensaio a 100 Hz)",
                       fontsize=12)
        eixo.legend(fontsize=10)
        fig.tight_layout()
        fig.savefig(PASTA_FIGURAS / f"blocos_degrau_{angulo}.png", dpi=300)
        plt.close(fig)

    fig.savefig(PASTA_FIGURAS / "resposta_degrau.png", dpi=300)
    plt.close(fig)
    print(f"figuras salvas em {PASTA_FIGURAS}")


if __name__ == "__main__":
    main()
