"""Ensaio cego em SERIES para repetibilidade e histerese.

REPETICOES ciclos; em cada ciclo: subida ANGULO_MIN->ANGULO_MAX seguida da
descida ANGULO_MAX->ANGULO_MIN. Cada degrau sai com REPETICOES medidas em
cada direcao (3 ciclos => 3 subidas + 3 descidas por degrau).

O angulo 95 (neutro) e' gravado como linha de base, sem exigir resposta
na corrente — o neutro nao produz corrente, e exigir resposta so' geraria
retentativas em vao.

A aquisicao roda na frequencia do firmware (~100 Hz), mas o CSV recebe
apenas 1 ponto por segundo (a media daquele segundo) — 15 pontos por
degrau, mesmo formato dos dados antigos de 1 Hz. O resumo (patinagem,
media pre-patinagem, fase de aderencia) continua usando todas as leituras.

CSV: mesmas 4 colunas dos demais ensaios (a direcao, subida ou descida,
e' inferida na analise pela ordem dos angulos). Modo append: interrompeu,
recarregou a bateria e rodou de novo — os dados se acumulam como series
extras.

Uso: python3 rodar_ensaio_series.py
"""

import csv
import os
import time
from serial import Serial

from rodar_ensaio import (BAUD, DURACAO_S, LOCK_PATH, PORTA_SERIAL,
                          enviar_comando, garantir_neutro, instancia_unica, log)
from rodar_ensaio_cego import (CABECALHO_CSV, aguardar_repouso,
                               disparar_e_medir, le_corrente)

# ---------------------------------------------------------------- config
REPETICOES = 3
ANGULO_MIN = 95
ANGULO_MAX = 117
NOME_CSV = "ensaio_series.csv"
PAUSA_S = 3                    # folga minima entre degraus (bateria/ESC)


def medir_baseline(ser, csv_writer, angulo, t_ensaio0):
    """Neutro (95): grava a linha de base, 1 ponto/s (media do segundo)."""
    log.info(">> DEGRAU %d (neutro): gravando linha de base", angulo)
    enviar_comando(angulo, DURACAO_S)
    t_ini = time.time()
    fim = t_ini + DURACAO_S
    seg_ant, soma_seg, n_seg = 0, 0.0, 0
    while time.time() < fim:
        i = le_corrente(ser)
        if i is None:
            continue
        soma_seg += i
        n_seg += 1
        seg = int(time.time() - t_ini)
        if seg > seg_ant:
            csv_writer.writerow([f"{time.time() - t_ensaio0:.1f}",
                                 f"{float(seg_ant):.1f}", angulo,
                                 f"{soma_seg / n_seg:.2f}"])
            seg_ant, soma_seg, n_seg = seg, 0.0, 0
    if n_seg:
        csv_writer.writerow([f"{time.time() - t_ensaio0:.1f}",
                             f"{float(seg_ant):.1f}", angulo,
                             f"{soma_seg / n_seg:.2f}"])
    log.info(">> baseline %d gravado (15 pontos/s)", angulo)


def main(repeticoes=REPETICOES, nome_csv=NOME_CSV):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    ciclos = []
    for k in range(1, repeticoes + 1):
        ciclos += [(k, a) for a in range(ANGULO_MIN, ANGULO_MAX + 1)]
        ciclos += [(k, a) for a in range(ANGULO_MAX, ANGULO_MIN - 1, -1)]

    n_degraus = len(ciclos)
    log.info("Plano: %d ciclos de %d->%d + %d->%d = %d degraus "
             "(~%.0f min)", repeticoes, ANGULO_MIN, ANGULO_MAX, ANGULO_MAX,
             ANGULO_MIN, n_degraus, n_degraus * (DURACAO_S + PAUSA_S + 1) / 60)

    with instancia_unica(LOCK_PATH):
        with Serial(PORTA_SERIAL, BAUD, timeout=3) as ser:
            time.sleep(2)
            ser.reset_input_buffer()

            t_ensaio0 = time.time()
            existe = os.path.exists(nome_csv) and os.path.getsize(nome_csv) > 0
            modo = "a" if existe else "w"
            with open(nome_csv, modo, buffering=1, newline="") as arq:
                csv_writer = csv.writer(arq, delimiter=";")
                if not existe:
                    csv_writer.writerow(CABECALHO_CSV.split(";"))
                try:
                    for k, angulo in ciclos:
                        log.info("### CICLO %d/%d | DEGRAU %d ###",
                                 k, repeticoes, angulo)
                        aguardar_repouso(ser)
                        if angulo <= 95:
                            medir_baseline(ser, csv_writer, angulo, t_ensaio0)
                        else:
                            disparar_e_medir(ser, csv_writer, angulo,
                                             t_ensaio0,
                                             gravar_por_segundo=True)
                        time.sleep(PAUSA_S)
                except KeyboardInterrupt:
                    log.warning("Interrompido; enviando neutro e fechando CSV.")
                    garantir_neutro()
                    return False
    log.info("Ensaio completo (%d ciclos). CSV salvo em %s",
             repeticoes, nome_csv)
    return True


if __name__ == "__main__":
    main()
