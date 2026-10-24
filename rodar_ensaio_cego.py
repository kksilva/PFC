"""Modo robusto/arcaico: dispara o throttle SEM confirmacao de rede e detecta a
resposta ELETRICAMENTE, na corrente da serial do Arduino.

Para quando a rede do Pi cai nos degraus altos (EMI/brown-out): o unico canal
confiavel e a serial local. A janela de cada degrau comeca no instante em que a
corrente responde, nao quando o Pi confirma. A rede, quando viva, so serve para
limpar processos orfaos (pkill) antes de cada disparo.

Uso: python3 rodar_ensaio_cego.py
"""

import csv
import os
import time
from collections import deque
from serial import Serial

from rodar_ensaio import (BAUD, DURACAO_S, INICIO_JANELA_S,
                          LOCK_PATH, MM_SEGUNDOS, NEUTRO_GRAUS, PORTA_SERIAL,
                          enviar_comando, extrair_corrente, garantir_neutro,
                          instancia_unica, limpar_pi, log, media,
                          medir_latencia, resumo_degrau)

# ---------------------------------------------------------------- config
ANGULO_INICIAL = 98
ANGULO_FINAL = 114
DIRECAO = "descida"            # "subida" | "descida"
NOME_CSV = "ensaio_cego_descida.csv"
LIMIAR_RESPOSTA_A = 0.3       # I acima disso = throttle respondeu (96-98 da
                              # ~0,5-1,5 A; ruído de repouso e +/-0,15 A)
LIMIAR_REPOUSO_A = 0.5        # |I| abaixo disso = repouso entre degraus
TENTATIVAS_CEGAS = 8          # disparos por degrau (cobre reboot ~60 s do Pi)
ESPERA_RESPOSTA_S = 10        # janela para a corrente responder apos cada disparo
PAUSA_ENTRE_DEGRAUS_S = 5
CABECALHO_CSV = "t_ensaio_s;t_degrau_s;angulo;corrente_a"


def le_corrente(ser):
    return extrair_corrente(ser.readline().decode(errors="replace"))


def aguardar_repouso(ser, timeout_s=20):
    """Espera a corrente ficar abaixo do limiar (fim do degrau anterior)."""
    fim = time.time() + timeout_s
    while time.time() < fim:
        i = le_corrente(ser)
        if i is not None and abs(i) < LIMIAR_REPOUSO_A:
            return True
    return False


def disparar_e_medir(ser, csv_writer, angulo, t_ensaio0, gravar_por_segundo=False):
    """Dispara (fogo-e-esqueca) ate a corrente responder; mede a janela a
    partir da resposta. Retorna True se o degrau foi executado.

    gravar_por_segundo=False: CSV recebe TODA leitura (~100 Hz).
    gravar_por_segundo=True : CSV recebe so a media de cada segundo
                              (15 pontos por degrau; a aquisicao continua
                              a 100 Hz e o resumo usa todas as leituras)."""
    ser.reset_input_buffer()
    t0 = primeira = None
    probar = True                # so sonda a rede ate ela falhar; depois dispara direto
    for tentativa in range(1, TENTATIVAS_CEGAS + 1):
        if probar:
            if medir_latencia() is not None:
                limpar_pi()      # rede viva: garante que so ha este throttle
            else:
                log.warning("rede morta; disparando no escuro ate ela voltar")
                probar = False
        enviar_comando(angulo, DURACAO_S)
        limite = time.time() + ESPERA_RESPOSTA_S
        while time.time() < limite:
            i = le_corrente(ser)
            if i is not None and i >= LIMIAR_RESPOSTA_A:
                t0, primeira = time.time(), i
                break
        if t0 is not None:
            break
        log.warning("degrau %d sem resposta na corrente; re-disparando (%d/%d)",
                    angulo, tentativa, TENTATIVAS_CEGAS)
        probar = True            # nova tentativa reavalia a rede
        time.sleep(3)

    if t0 is None:
        log.error("DEGRAU %d NAO executado apos %d disparos; pulado",
                  angulo, TENTATIVAS_CEGAS)
        return False

    log.info(">> DEGRAU %d: resposta em %.1f s (I=%.2f A); medindo %d s",
             angulo, t0 - t_ensaio0, primeira, DURACAO_S)
    leituras = [(0.0, primeira)]
    if not gravar_por_segundo:
        csv_writer.writerow([f"{t0 - t_ensaio0:.1f}", "0.0", angulo,
                             f"{primeira:.2f}"])
    print(f"  t=0s | I={primeira:.2f} A (resposta)", flush=True)

    fim = t0 + DURACAO_S
    seg_ant, soma_seg, n_seg = 0, 0.0, 0
    mm_seg = deque(maxlen=MM_SEGUNDOS)
    while time.time() < fim:
        i = le_corrente(ser)
        if i is None:
            continue
        t = time.time() - t0
        if not gravar_por_segundo:
            csv_writer.writerow([f"{time.time() - t_ensaio0:.1f}", f"{t:.1f}",
                                 angulo, f"{i:.2f}"])
        leituras.append((t, i))
        soma_seg += i
        n_seg += 1
        seg = int(t)
        if seg > seg_ant:
            m_seg = soma_seg / n_seg
            mm_seg.append(m_seg)
            if gravar_por_segundo:
                csv_writer.writerow([f"{time.time() - t_ensaio0:.1f}",
                                     f"{float(seg_ant):.1f}", angulo,
                                     f"{m_seg:.2f}"])
            print(f"  t={seg_ant}s | I={m_seg:.2f} A | MM={media(mm_seg):.2f} A",
                  flush=True)
            seg_ant, soma_seg, n_seg = seg, 0.0, 0
    if n_seg:
        m_seg = soma_seg / n_seg
        mm_seg.append(m_seg)
        if gravar_por_segundo:
            csv_writer.writerow([f"{time.time() - t_ensaio0:.1f}",
                                 f"{float(seg_ant):.1f}", angulo,
                                 f"{m_seg:.2f}"])
        print(f"  t={seg_ant}s | I={m_seg:.2f} A | MM={media(mm_seg):.2f} A",
              flush=True)

    garantir_neutro() if medir_latencia() is not None else enviar_comando(NEUTRO_GRAUS, 2)
    resumo_degrau(angulo, leituras)
    return True


def main(direcao=DIRECAO, nome_csv=NOME_CSV,
         angulo_inicial=ANGULO_INICIAL, angulo_final=ANGULO_FINAL):
    if direcao == "descida":
        escada = range(angulo_final, angulo_inicial - 1, -1)
    else:
        escada = range(angulo_inicial, angulo_final + 1)

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
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
                    for angulo in escada:
                        aguardar_repouso(ser)
                        disparar_e_medir(ser, csv_writer, angulo, t_ensaio0)
                        time.sleep(PAUSA_ENTRE_DEGRAUS_S)
                except KeyboardInterrupt:
                    log.warning("Interrompido; enviando neutro e fechando CSV.")
                    garantir_neutro()
                    return False
    log.info("Ensaio completo. CSV salvo em %s", nome_csv)
    return True


if __name__ == "__main__":
    main()
