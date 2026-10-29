"""Simulacao da cascata de controle de torque do automodelo (PSR / PRP / seletor).

Le a caracterizacao estatica (ensaio_tracao_corrente_versus_forca.xlsx (pasta reprodutibilidade)), ajusta a planta nao-linear
da corrente e o ganho de torque diretamente dos dados (sem reducao i, sem K_t),
executa a simulacao da cascata mestre (torque estimado) / escrava (corrente) com
todas as nao-linearidades e salvaguardas do projeto, e gera a figura
PFC_monografia/Figuras/simulacao_cascata.png.

Uso:  python3 simulacao_cascata.py
Saida: figura PNG + metricas PSR/PRP impressas no terminal.
"""

# ---------------------------------------------------------------------------
# MAPA
# 1) Constantes do projeto: ajuste da planta, sintese IMC, salvaguardas e cenario de simulacao (linhas 30-74)
# 2) Leitura e ajuste dos dados de ensaio: repeticoes da descida, I0(u), planta I_ss(u), ganho de torque, comando equivalente (linhas 76-160)
# 3) Simulacao da cascata: ganhos IMC, cenario PSR/PRP/seletor, estimador, seletor, mestre, caminho direto com feedforward, PI escravo com clamping, planta (linhas 163-261)
# 4) Metricas PSR/PRP/retorno/seletor e figura simulacao_cascata.png (linhas 264-372)
# ---------------------------------------------------------------------------

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import openpyxl

# --------------------------------------------------------------------------- #
# Constantes do projeto (identificadas nos ensaios)
# --------------------------------------------------------------------------- #
PASTA_ENSAIOS = Path(__file__).resolve().parent
PASTA_FIGURAS = Path(__file__).resolve().parent
# (na pasta reprodutibilidade, as figuras saem junto aos scripts)

PLANILHA_DADOS = PASTA_ENSAIOS / "ensaio_tracao_corrente_versus_forca.xlsx"
ABA_PLANILHA = "P\xe1gina1"

DEGRAU_MINIMO = 100          # faixa de ajuste: regiao de aderencia (descida)
DEGRAU_MAXIMO = 113
ANGULO_NEUTRO_GRAUS = 95.0   # u = (angulo - neutro) / faixa_total
FAIXA_COMANDO = 85.0
RAIO_EFETIVO_M = 0.0751      # roll-out (metodologia)

CONSTANTE_TEMPO_PLANTA_S = 0.18   # dinamica comando->corrente (ensaio de tracao de corrente)

# Controladores (sintese IMC, conforme planejamento do controle)
LAMBDA_ESCRAVA_S = 0.18           # malha de corrente: tao rapida quanto a planta
LAMBDA_MESTRE_S = 1.1             # regra da cascata: 3-10x mais lenta (6x)
TEMPO_INTEGRAL_ESCRAVA_S = CONSTANTE_TEMPO_PLANTA_S
TEMPO_INTEGRAL_MESTRE_S = 0.18
TEMPO_AMOSTRAGEM_S = 0.01         # firmware rapido (<= Ti/10)

# Salvaguardas (cada uma justificada por um modo de falha, ver planejamento)
COMANDO_MIN = 0.045               # limite inferior: saida da zona morta
COMANDO_MAX = 0.21                # fronteira da regiao de aderencia validada
TORQUE_MAXIMO_SELETOR_NM = 3.3    # limiar de aderencia (forca max. x r_ef)
TORQUE_MAXIMO_ESTIMADOR_NM = 3.35 # estimador valido so onde foi caracterizado
RAMPA_CAMINHO_DIRETO_U_POR_S = 0.05
RAMPA_REFERENCIA_MESTRE_NM_POR_S = 0.6
CONSTANTE_FILTRO_ESTIMADOR_S = 0.6

# Cenario de simulacao
TEMPO_FINAL_S = 64.0
TORQUE_INICIAL_NM = 1.6
TORQUE_PSR_NM = 3.0
TORQUE_SELETOR_NM = 4.5
INSTANTE_PSR_S, INSTANTE_PRP_S = 10.0, 24.0
DURACAO_PRP_S = 6.0               # sag + deslocamento de I0 entre 24 e 30 s
INSTANTE_RETORNO_S, INSTANTE_SELETOR_S = 38.0, 48.0
QUEDA_GANHO_PRP = 0.8             # sag de 20% na planta
DESLOCAMENTO_I0_PRP_A = 0.3


# --------------------------------------------------------------------------- #
# Leitura e ajuste dos dados de ensaio
# --------------------------------------------------------------------------- #
def carregar_repeticoes_descida(caminho_planilha):
    """Retorna dicionario {degrau: (correntes_A, forcas_kgf)} das repeticoes."""
    # So a descida e usada: e o sentido em que a caracteristica foi validada
    # ate a saturacao, sem os pontos de corte do ESC que contaminam a subida.
    planilha = openpyxl.load_workbook(caminho_planilha, data_only=True)
    pagina = planilha[ABA_PLANILHA]
    linhas = list(pagina.iter_rows(values_only=True))
    cabecalho = linhas[0]
    degraus = [int(cabecalho[i]) for i in range(1, 44, 2) if cabecalho[i] is not None]
    repeticoes = []
    for linha in linhas[2:]:
        if linha[0] != "DESCIDA":
            continue
        pares = {}
        for j, degrau in enumerate(degraus):
            corrente, forca = linha[1 + 2 * j], linha[2 + 2 * j]
            if corrente is not None and forca is not None:
                pares[degrau] = (float(corrente), float(forca))
        repeticoes.append(pares)
    return repeticoes


def comando_normalizado(degrau):
    """u = (angulo - neutro) / faixa, conforme a metodologia."""
    return (degrau - ANGULO_NEUTRO_GRAUS) / FAIXA_COMANDO


# Corrente de perdas I0(u) = I0_A + I0_B u, ajustada no ensaio em vazio
# (Apendice A, analise_estatica.py)
I0_A = 0.53
I0_B = 6.70


def corrente_perdas_a(u):
    """I0(u) ajustado no ensaio em vazio: I0 = 0,53 + 6,70 u."""
    return I0_A + I0_B * u


def ajustar_planta_corrente(repeticoes):
    """Planta estatica I_ss(u): quadratica sobre a descida, regiao de aderencia."""
    # A corrente de regime nao e linear no comando (ganho cai na saturacao);
    # um ajuste quadratico sobre a regiao de aderencia captura essa curvatura
    # com os dados brutos das repeticoes, sem reducao intermediaria.
    comodos, correntes = [], []
    for rep in repeticoes:
        for degrau in range(DEGRAU_MINIMO, DEGRAU_MAXIMO + 1):
            if degrau in rep:
                comodos.append(comando_normalizado(degrau))
                correntes.append(rep[degrau][0])
    coeficientes = np.polyfit(np.array(comodos), np.array(correntes), 2)
    return coeficientes  # I_ss(u) = c2 u^2 + c1 u + c0


def ajustar_ganho_torque(repeticoes):
    """K_T da relacao F = G_F (I - I0(u))/u, ajustada pela origem (sem i, sem K_t).

    Retorna K_T = G_F * r_ef, em N*m por (A/u).
    """
    eixo_x, eixo_y = [], []
    for rep in repeticoes:
        for degrau in range(DEGRAU_MINIMO, DEGRAU_MAXIMO + 1):
            if degrau in rep:
                u = comando_normalizado(degrau)
                corrente, forca_kgf = rep[degrau]
                eixo_x.append((corrente - corrente_perdas_a(u)) / u)
                eixo_y.append(forca_kgf * 9.81)
    eixo_x, eixo_y = np.array(eixo_x), np.array(eixo_y)
    ganho_forca = float((eixo_x * eixo_y).sum() / (eixo_x * eixo_x).sum())
    return ganho_forca * RAIO_EFETIVO_M


def comando_equivalente(torque_desejado, coef_planta, ganho_torque):
    """Inverte a curva estatica: u tal que K_T (I_ss(u) - I0(u))/u = torque."""
    # A inversao analitica (raiz do polinomio) e o caminho direto do
    # feedforward: posiciona o comando no ponto de equilibrio do torque
    # pedido, deixando ao PI escravo apenas o desvio.
    c2, c1, c0 = coef_planta
    coeficientes = [c2, (c1 - I0_B) - torque_desejado / ganho_torque, c0 - I0_A]
    raizes = np.roots(coeficientes)
    validas = [r.real for r in raizes
               if np.isreal(r) and COMANDO_MIN - 0.015 < r.real < 0.5]
    return min(validas) if validas else COMANDO_MIN


# --------------------------------------------------------------------------- #
# Simulacao da cascata
# --------------------------------------------------------------------------- #
# Passo a passo de 10 ms, com o cenario PSR/PRP/seletor injetado como funcoes
# do tempo e todas as salvaguardas do projeto ativas. A ordem de cada passo e:
# estimador, seletor+rampa, mestre, caminho direto com feedforward, escravo com
# clamping e, por fim, a planta.


def simular_cascata(coef_planta, ganho_torque):
    c2, c1, c0 = coef_planta
    ganho_local = 2 * c2 * comando_normalizado(105) + c1   # dI/du no nominal
    kp_escrava = CONSTANTE_TEMPO_PLANTA_S / (ganho_local * LAMBDA_ESCRAVA_S)
    kp_mestre = lambda u: (CONSTANTE_TEMPO_PLANTA_S * u
                           / (ganho_torque * LAMBDA_MESTRE_S))

    n_passos = int(TEMPO_FINAL_S / TEMPO_AMOSTRAGEM_S)
    tempos = np.arange(n_passos) * TEMPO_AMOSTRAGEM_S

    def referencia_pedida(tempo):
        if tempo < INSTANTE_PSR_S:
            return TORQUE_INICIAL_NM
        if tempo < INSTANTE_RETORNO_S:
            return TORQUE_PSR_NM
        if tempo < INSTANTE_SELETOR_S:
            return TORQUE_INICIAL_NM
        return TORQUE_SELETOR_NM

    def perturbacao_presente(tempo):
        em_prp = INSTANTE_PRP_S <= tempo < INSTANTE_PRP_S + DURACAO_PRP_S
        return (QUEDA_GANHO_PRP if em_prp else 1.0,
                DESLOCAMENTO_I0_PRP_A if em_prp else 0.0)

    # Estado inicial consistente (ponto de equilibrio do torque inicial)
    comando = comando_equivalente(TORQUE_INICIAL_NM, coef_planta, ganho_torque)
    corrente = float(np.polyval(coef_planta, comando))
    integral_mestre, integral_escrava = 0.0, 0.0
    comando_direto = comando
    torque_filtrado = TORQUE_INICIAL_NM
    referencia_mestre = TORQUE_INICIAL_NM

    historico = {chave: np.zeros(n_passos) for chave in
                 ("torque", "corrente", "comando", "referencia", "referencia_mestre")}

    for passo in range(n_passos):
        tempo = tempos[passo]
        comando_efetivo = max(comando, COMANDO_MIN)
        fator_ganho, deslocamento_i0 = perturbacao_presente(tempo)

        # estimador de torque (quase-estatico, limitado a faixa validada)
        torque_bruto = ganho_torque * (corrente - corrente_perdas_a(comando_efetivo)
                                       - deslocamento_i0) / comando_efetivo
        torque_estimado = min(max(torque_bruto, 0.0), TORQUE_MAXIMO_ESTIMADOR_NM)
        torque_filtrado += ((torque_estimado - torque_filtrado)
                            * TEMPO_AMOSTRAGEM_S / CONSTANTE_FILTRO_ESTIMADOR_S)

        # seletor de aderencia + filtro de referencia do mestre
        referencia = min(referencia_pedida(tempo), TORQUE_MAXIMO_SELETOR_NM)
        passo_rampa = RAMPA_REFERENCIA_MESTRE_NM_POR_S * TEMPO_AMOSTRAGEM_S
        referencia_mestre += min(max(referencia - referencia_mestre, -passo_rampa),
                                 passo_rampa)

        # controlador mestre (torque -> correcao de corrente)
        erro_mestre = referencia_mestre - torque_filtrado
        correcao_corrente = kp_mestre(comando_efetivo) * (erro_mestre + integral_mestre)

        # caminho direto: comando equivalente (com rampa) + feedforward de corrente
        passo_direto = RAMPA_CAMINHO_DIRETO_U_POR_S * TEMPO_AMOSTRAGEM_S
        alvo_direto = comando_equivalente(referencia, coef_planta, ganho_torque)
        comando_direto += min(max(alvo_direto - comando_direto, -passo_direto),
                              passo_direto)
        corrente_referencia = (corrente_perdas_a(comando_efetivo)
                               + comando_efetivo * referencia / ganho_torque
                               + correcao_corrente)

        # controlador escravo (corrente -> comando), com anti-windup por clamping
        erro_escrava = corrente_referencia - corrente
        comando_nao_limitado = comando_direto + kp_escrava * (erro_escrava + integral_escrava)
        comando = min(max(comando_nao_limitado, COMANDO_MIN), COMANDO_MAX)
        saturado = abs(comando - comando_nao_limitado) > 1e-9
        if saturado:
            # clamping: ajusta o integral para a saida ficar exatamente no limite
            integral_escrava = (comando - comando_direto) / kp_escrava - erro_escrava
        else:
            integral_escrava += erro_escrava * TEMPO_AMOSTRAGEM_S / TEMPO_INTEGRAL_ESCRAVA_S
            integral_mestre += erro_mestre * TEMPO_AMOSTRAGEM_S / TEMPO_INTEGRAL_MESTRE_S

        # planta nao-linear da corrente (curva estatica + 1a ordem)
        corrente_estatica = max(float(np.polyval(coef_planta, comando_efetivo)), 0.0)
        corrente += ((corrente_estatica * fator_ganho - corrente)
                     / CONSTANTE_TEMPO_PLANTA_S) * TEMPO_AMOSTRAGEM_S

        historico["torque"][passo] = torque_estimado
        historico["corrente"][passo] = corrente
        historico["comando"][passo] = comando
        historico["referencia"][passo] = referencia_pedida(tempo)
        historico["referencia_mestre"][passo] = referencia_mestre

    return tempos, historico


# --------------------------------------------------------------------------- #
# Metricas e figura
# --------------------------------------------------------------------------- #
# As metricas leem o torque estimado nos trechos de cada transicao (media de
# 0,5 s antes do instante indicado) e alimentam os resultados PSR/PRP da
# monografia.


def amostra_media(vetor, tempo, alvo_s, janela_s=0.5):
    fim = int(alvo_s / TEMPO_AMOSTRAGEM_S)
    inicio = fim - int(janela_s / TEMPO_AMOSTRAGEM_S)
    return vetor[inicio:fim].mean()


def imprimir_metricas(tempos, historico):
    torque = historico["torque"]
    i_psr = int(INSTANTE_PSR_S / TEMPO_AMOSTRAGEM_S)
    i_prp = int(INSTANTE_PRP_S / TEMPO_AMOSTRAGEM_S)
    i_fim_prp = int((INSTANTE_PRP_S + DURACAO_PRP_S) / TEMPO_AMOSTRAGEM_S)

    trecho_psr = torque[i_psr:i_prp]
    amplitude = TORQUE_PSR_NM - TORQUE_INICIAL_NM
    pico = trecho_psr.max()
    print(f"PSR {TORQUE_INICIAL_NM}->{TORQUE_PSR_NM} N.m: "
          f"pico={pico:.2f} N.m (Mp={max((pico - TORQUE_PSR_NM) / amplitude * 100, 0):.0f}%) | "
          f"T({INSTANTE_PSR_S + 5.5:.1f}s)={amostra_media(torque, tempos, INSTANTE_PSR_S + 5.5):.3f} N.m")
    print(f"PRP (sag 20% + I0 +0,3 A): "
          f"desvio max={abs(torque[i_prp:i_fim_prp].min() - TORQUE_PSR_NM):.2f} N.m | "
          f"regime={amostra_media(torque, tempos, INSTANTE_PRP_S + DURACAO_PRP_S + 1.5):.3f} N.m (ref {TORQUE_PSR_NM})")
    print(f"retorno: T({INSTANTE_RETORNO_S + 5.5:.1f}s)={amostra_media(torque, tempos, INSTANTE_RETORNO_S + 5.5):.3f} N.m "
          f"(ref {TORQUE_INICIAL_NM})")
    print(f"seletor: T({INSTANTE_SELETOR_S + 13.0:.1f}s)={amostra_media(torque, tempos, INSTANTE_SELETOR_S + 13.0):.2f} N.m "
          f"(limite {TORQUE_MAXIMO_SELETOR_NM})")


def gerar_figura(tempos, historico, caminho_saida):
    # Tres eixos empilhados (torque, corrente, comando) ao longo de 64 s, com as
    # janelas de cada cenario sombreadas: cada degrau so e aplicado apos o regime
    # permanente do cenario anterior.
    plt.rcParams.update({"font.size": 12, "axes.grid": True,
                         "grid.alpha": 0.25, "axes.axisbelow": True,
                         "axes.titlesize": 14, "legend.framealpha": 0.95})
    fig, eixos = plt.subplots(3, 1, figsize=(10.2, 7.6), sharex=True)

    janelas = [
        (INSTANTE_PSR_S, INSTANTE_PRP_S, "#d1e5f0", "PSR: $1{,}6 \\rightarrow 3{,}0$ N.m"),
        (INSTANTE_PRP_S, INSTANTE_PRP_S + DURACAO_PRP_S, "#f4a582",
         "PRP: sag $-20\\%$ + $I_0$ $+0{,}3$ A"),
        (INSTANTE_RETORNO_S, INSTANTE_SELETOR_S, "#d9f0d3",
         "retorno: $3{,}0 \\rightarrow 1{,}6$ N.m"),
        (INSTANTE_SELETOR_S, TEMPO_FINAL_S, "#e0d4e8",
         "seletor: pedido $4{,}5$ N.m"),
    ]
    for eixo in eixos:
        for inicio_j, fim_j, cor, _ in janelas:
            eixo.axvspan(inicio_j, fim_j, color=cor, alpha=0.55, zorder=0)

    eixos[0].plot(tempos, historico["referencia"], "k--", lw=1.2,
                  label="$T_\\mathrm{ref}$ pedida")
    eixos[0].plot(tempos, historico["torque"], color="#2166ac", lw=1.8,
                  label="$\\hat{T}$ (torque estimado)")
    eixos[0].axhline(TORQUE_MAXIMO_SELETOR_NM, color="#b2182b", ls=":", lw=1.2)
    eixos[0].text(0.6, TORQUE_MAXIMO_SELETOR_NM + 0.12,
                  "limiar do seletor (3,3 N.m)", fontsize=9.5, color="#b2182b")
    eixos[0].set_ylabel("Torque (N.m)")
    eixos[0].set_title("Simulacao da cascata de torque: cenario PSR / PRP / retorno / seletor")
    eixos[0].set_ylim(0.8, 5.2)
    eixos[0].legend(fontsize=10.5, loc="center right")

    i_pico = int(np.argmax(historico["torque"][:int(INSTANTE_PRP_S / TEMPO_AMOSTRAGEM_S)]))
    eixos[0].annotate(f"pico {historico['torque'][i_pico]:.2f} N.m\n(Mp = 25%)",
                      xy=(tempos[i_pico], historico["torque"][i_pico]),
                      xytext=(tempos[i_pico] + 3.0, 4.05),
                      fontsize=9.5, ha="left",
                      arrowprops=dict(arrowstyle="->", lw=0.9, color="0.25"))
    i_prp = int((INSTANTE_PRP_S + 1.0) / TEMPO_AMOSTRAGEM_S)
    desvio = abs(historico["torque"][int(INSTANTE_PRP_S / TEMPO_AMOSTRAGEM_S)
                                   :int((INSTANTE_PRP_S + DURACAO_PRP_S)
                                        / TEMPO_AMOSTRAGEM_S)].min() - TORQUE_PSR_NM)
    eixos[0].annotate(f"desvio max.\n{desvio:.2f} N.m",
                      xy=(tempos[i_prp], historico["torque"][i_prp]),
                      xytext=(INSTANTE_PRP_S + 0.4, 2.1),
                      fontsize=9.5, ha="left",
                      arrowprops=dict(arrowstyle="->", lw=0.9, color="0.25"))

    eixos[1].plot(tempos, historico["corrente"], color="#b2182b", lw=1.4,
                  label="Corrente $I$")
    eixos[1].set_ylabel("Corrente (A)")
    eixos[1].legend(fontsize=10.5, loc="center right")

    eixos[2].plot(tempos, historico["comando"], color="#1b7837", lw=1.4,
                  label="Comando $u$")
    eixos[2].axhline(COMANDO_MAX, color="0.6", ls=":", lw=0.9)
    eixos[2].set_ylabel("Comando $u$")
    eixos[2].set_xlabel("Tempo (s)")
    eixos[2].set_xlim(0, TEMPO_FINAL_S)
    eixos[2].legend(fontsize=10.5, loc="center right")

    for inicio_j, fim_j, _, nome in janelas:
        eixos[0].text((inicio_j + fim_j) / 2, 5.0, nome, ha="center", va="top",
                      fontsize=10, style="italic")
    for eixo in eixos:
        for inicio_j, fim_j, _, _ in janelas:
            eixo.axvline(inicio_j, color="0.5", lw=0.9, ls=(0, (4, 3)), zorder=1)

    fig.tight_layout()
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(caminho_saida, dpi=300)
    plt.close(fig)
    print(f"figura salva em {caminho_saida}")


def main():
    # Pipeline: ajusta planta e ganho a partir das repeticoes da descida,
    # simula a cascata, imprime as metricas e gera a figura.
    repeticoes = carregar_repeticoes_descida(PLANILHA_DADOS)
    coef_planta = ajustar_planta_corrente(repeticoes)
    ganho_torque = ajustar_ganho_torque(repeticoes)
    print(f"planta I_ss(u) = {coef_planta[0]:.1f} u^2 + {coef_planta[1]:.1f} u "
          f"{coef_planta[2]:.2f} | K_T = {ganho_torque:.4f} N.m/(A/u)")

    tempos, historico = simular_cascata(coef_planta, ganho_torque)
    imprimir_metricas(tempos, historico)
    gerar_figura(tempos, historico, PASTA_FIGURAS / "simulacao_cascata.png")


if __name__ == "__main__":
    main()
