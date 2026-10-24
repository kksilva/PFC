"""Ensaio em SERIES com o comando ssh ORIGINAL — sem tunel, sem multiplexacao.

Cada iteracao executa exatamente:
    ssh alunos@raspberrypi.local "python3 /home/alunos/teste_throttle.py <degrau> <duracao>"

Uma conexao ssh NOVA por degrau: nao ha soquete mestre para apodrecer, nao ha
probing de rede, nao ha retentativa. Se o Pi estiver inalcancavel, o comando
falha sozinho e o degrau grava a linha de base (corrente ~0) — a analise
descarta pelo plato.

Enquanto o comando roda, a serial do Arduino e lida e o CSV recebe 1 ponto por
segundo (a media da corrente naquele segundo); o terminal imprime a mesma
linha com a media movel. A janela cobre DURACAO_S + EXTRAS_S (o Pi arma o ESC
com ~2-3 s de neutro antes do throttle).

Plano: REPETICOES ciclos; cada ciclo = subida ANGULO_MIN->ANGULO_MAX seguida
da descida ANGULO_MAX->ANGULO_MIN.

Uso: python3 rodar_ensaio_series.py
"""

import csv
import os
import subprocess
import time
from collections import deque
from serial import Serial

from rodar_ensaio import (BAUD, LOCK_PATH, MM_SEGUNDOS, PORTA_SERIAL,
                          extrair_corrente, instancia_unica, log, media,
                          resumo_degrau)

# ---------------------------------------------------------------- config
REPETICOES = 3
ANGULO_MIN = 95
ANGULO_MAX = 117
DURACAO_S = 15               # throttle por degrau (o exemplo usava 3: ajuste aqui)
EXTRAS_S = 4                 # cobre o neutro de armamento do ESC antes do throttle
PAUSA_S = 3                  # folga entre degraus
NOME_CSV = "ensaio_series.csv"
PI = "alunos@raspberrypi.local"
COMANDO = "python3 /home/alunos/teste_throttle.py"
CABECALHO_CSV = "t_ensaio_s;t_degrau_s;angulo;corrente_a"


def medir_janela(ser, csv_writer, angulo, t0, t_ensaio0, duracao):
    """Le a serial por 'duracao' s a partir de t0; grava e imprime 1 ponto/s
    (media do segundo, com media movel no terminal). Retorna todas as leituras."""
    fim = t0 + duracao
    seg_ant, soma_seg, n_seg = 0, 0.0, 0
    mm_seg = deque(maxlen=MM_SEGUNDOS)
    leituras = []
    while time.time() < fim:
        i = extrair_corrente(ser.readline().decode(errors="replace"))
        if i is None:
            continue
        t = time.time() - t0
        leituras.append((t, i))
        soma_seg += i
        n_seg += 1
        seg = int(t)
        if seg > seg_ant:
            m_seg = soma_seg / n_seg
            mm_seg.append(m_seg)
            csv_writer.writerow([f"{time.time() - t_ensaio0:.1f}",
                                 f"{float(seg_ant):.1f}", angulo,
                                 f"{m_seg:.2f}"])
            print(f"  t={seg_ant}s | I={m_seg:.2f} A | MM={media(mm_seg):.2f} A",
                  flush=True)
            seg_ant, soma_seg, n_seg = seg, 0.0, 0
    if n_seg:
        m_seg = soma_seg / n_seg
        mm_seg.append(m_seg)
        csv_writer.writerow([f"{time.time() - t_ensaio0:.1f}",
                             f"{float(seg_ant):.1f}", angulo, f"{m_seg:.2f}"])
        print(f"  t={seg_ant}s | I={m_seg:.2f} A | MM={media(mm_seg):.2f} A",
              flush=True)
    return leituras


def executar_degrau(ser, csv_writer, angulo, t_ensaio0):
    """Dispara o comando ssh original e mede a janela."""
    log.info("### DEGRAU %d ###", angulo)
    ser.reset_input_buffer()
    t0 = time.time()
    proc = subprocess.Popen(["ssh", PI, f"{COMANDO} {angulo} {DURACAO_S}"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    leituras = medir_janela(ser, csv_writer, angulo, t0, t_ensaio0,
                            DURACAO_S + EXTRAS_S)
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
    resumo_degrau(angulo, leituras)
    time.sleep(PAUSA_S)


def neutro_final():
    """Neutro de seguranca no Ctrl+C (comando original, limite curto)."""
    try:
        subprocess.run(["ssh", PI, f"{COMANDO} 95 2"],
                       capture_output=True, timeout=12)
        log.info("neutro enviado")
    except subprocess.TimeoutExpired:
        log.warning("neutro NAO enviado (Pi inalcancavel); se o throttle estiver "
                    "ativo no Pi, interrompa pela chave de comutacao")


def main(repeticoes=REPETICOES, nome_csv=NOME_CSV):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    ciclos = []
    for k in range(1, repeticoes + 1):
        ciclos += [(k, a) for a in range(ANGULO_MIN, ANGULO_MAX + 1)]
        ciclos += [(k, a) for a in range(ANGULO_MAX, ANGULO_MIN - 1, -1)]

    n = len(ciclos)
    log.info("Plano: %d ciclos | %d degraus | ~%.0f min", repeticoes, n,
             n * (DURACAO_S + EXTRAS_S + PAUSA_S + 1) / 60)

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
                        executar_degrau(ser, csv_writer, angulo, t_ensaio0)
                except KeyboardInterrupt:
                    log.warning("Interrompido; enviando neutro e fechando CSV.")
                    neutro_final()
                    return False
    log.info("Ensaio completo (%d ciclos). CSV salvo em %s", repeticoes, nome_csv)
    return True


if __name__ == "__main__":
    main()
