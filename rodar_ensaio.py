"""Ensaio de caracterizacao torque x corrente do automodelo.

Aplica degraus de throttle via Raspberry Pi (teste_throttle.py), le a
corrente do ACS758 na serial do Arduino Due e grava um CSV linha a
linha. A janela de 15 s de cada degrau so comeca quando o Pi confirma
o comando, garantindo que t=0 seja o instante real em que o ESC
recebeu o throttle.
"""

import csv
import fcntl
import logging
import os
import select
import subprocess
import sys
import time
from contextlib import contextmanager
from serial import Serial

# ---------------------------------------------------------------- config do ensaio
ANGULO_INICIAL = 105          # primeiro degrau da escada
ANGULO_FINAL = 115            # ultimo degrau da escada
DURACAO_S = 15                # duracao de cada degrau
DIRECAO = "subida"            # "subida": INICIAL->FINAL | "descida": FINAL->INICIAL
NOME_CSV = "ensaio_subida_2.csv"
RETENTATIVAS = 3              # tentativas de confirmacao do Pi antes de pular o degrau
INICIO_JANELA_S = 7           # t_degrau a partir do qual o regime e valido (media final)

# ---------------------------------------------------------------- hardware
PORTA_SERIAL = "/dev/ttyACM0"
BAUD = 115200
PI = "alunos@raspberrypi.local"
COMANDO_PI = "python3 /home/alunos/teste_throttle.py"
NEUTRO_GRAUS = 95             # angulo de neutro do ESC

# ---------------------------------------------------------------- calibracao ACS758 (3,3 V)
V_REF = 3.3
ADC_MAX = 4095.0
OFFSET_V = 1.65
SENSIBILIDADE_V_A = 0.0066

# ---------------------------------------------------------------- infra
SSH_TUNNEL_OPTS = ["-o", "ControlMaster=auto",
                   "-o", "ControlPersist=600",
                   "-o", "ControlPath=/tmp/pfc-ssh.sock",
                   "-o", "ConnectTimeout=10",
                   "-o", "ServerAliveInterval=5",
                   "-o", "ServerAliveCountMax=2",
                   "-o", "BatchMode=yes"]
TIMEOUT_CONFIRMACAO_S = 25
LOCK_PATH = ".rodar_ensaio.lock"
CABECALHO_CSV = "t_ensaio_s;t_degrau_s;angulo;corrente_a"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s",
                    datefmt="%H:%M:%S", stream=sys.stdout)
log = logging.getLogger("ensaio")


# ---------------------------------------------------------------- utilitarios
@contextmanager
def instancia_unica(caminho_lock):
    """Impede que dois ensaios rodem juntos dividindo a porta serial."""
    lock = open(caminho_lock, "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        raise SystemExit("ERRO: outra instancia do script ja esta rodando. Feche-a antes.")
    try:
        yield
    finally:
        lock.close()


def extrair_corrente(linha):
    """Converte uma linha da serial em amperes; None se nao for leitura."""
    if "Corrente:" in linha:
        return float(linha.split("Corrente:")[1].split()[0])
    if "ADC:" in linha:
        adc = float(linha.split("ADC:")[1].split()[0])
        return (adc * V_REF / ADC_MAX - OFFSET_V) / SENSIBILIDADE_V_A
    return None


def media(valores):
    return sum(valores) / len(valores) if valores else float("nan")


# ---------------------------------------------------------------- comunicacao com o Pi
def aquecer_tunel():
    """Abre a conexao mestra ssh uma unica vez; os degraus reutilizam."""
    log.info("Conectando com o Raspberry Pi...")
    subprocess.run(["ssh", "-Nf"] + SSH_TUNNEL_OPTS + [PI], timeout=20)
    log.info("Tunel pronto.")


def enviar_comando(angulo, duracao_s):
    """Lanca o comando no Pi; retorna o processo ssh (stdout capturado)."""
    return subprocess.Popen(["ssh"] + SSH_TUNNEL_OPTS + [PI, COMANDO_PI,
                                                         str(angulo), str(duracao_s)],
                            stdout=subprocess.PIPE, text=True)


def aguardar_confirmacao(proc):
    """Espera o Pi confirmar 'Throttle:'; retorna o t0 real ou None."""
    limite = time.time() + TIMEOUT_CONFIRMACAO_S
    while time.time() < limite:
        prontos, _, _ = select.select([proc.stdout], [], [], 1)
        if not prontos:
            continue
        saida = proc.stdout.readline()
        if not saida:
            return None
        log.info("pi> %s", saida.strip())
        if "Throttle:" in saida:
            return time.time()
    return None


def garantir_neutro():
    """Forca o ESC de volta ao neutro (seguranca do veiculo)."""
    subprocess.run(["ssh"] + SSH_TUNNEL_OPTS + [PI, COMANDO_PI,
                                                str(NEUTRO_GRAUS), "2"])


# ---------------------------------------------------------------- nucleo do ensaio
def rodar_degrau(ser, csv_writer, angulo, t_ensaio0):
    """Aplica um degrau, sincroniza com o Pi, le a serial e grava.
    Retorna True se o degrau foi executado e confirmado."""
    log.info("### DEGRAU %d ###", angulo)

    t0 = None
    for tentativa in range(1, RETENTATIVAS + 1):
        proc = enviar_comando(angulo, DURACAO_S)
        t0 = aguardar_confirmacao(proc)
        if t0 is not None:
            break
        proc.kill()
        log.warning("tentativa %d/%d sem confirmacao; reenviando",
                    tentativa, RETENTATIVAS)
        time.sleep(2)

    if t0 is None:
        log.warning("Pi nao confirmou apos %d tentativas; degrau %d pulado",
                    RETENTATIVAS, angulo)
        garantir_neutro()
        time.sleep(3)
        return False

    ser.reset_input_buffer()   # so le o que for deste degrau
    leituras = []              # (t_degrau, corrente) para o resumo final
    fim = t0 + DURACAO_S
    while time.time() < fim:
        corrente = extrair_corrente(ser.readline().decode(errors="replace"))
        if corrente is None:
            continue
        t_degrau = time.time() - t0
        csv_writer.writerow([f"{time.time() - t_ensaio0:.1f}", f"{t_degrau:.1f}",
                             angulo, f"{corrente:.2f}"])
        leituras.append((t_degrau, corrente))
        print(f"  t={t_degrau:.1f}s | I={corrente:.2f} A", flush=True)

    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill()
        log.warning("Pi nao confirmou o neutro; reenviando")
        garantir_neutro()

    regime = [i for t, i in leituras if t >= INICIO_JANELA_S]
    log.info(">> DEGRAU %d: media janela %d-%ds = %.2f A (n=%d)",
             angulo, INICIO_JANELA_S, DURACAO_S, media(regime), len(regime))
    time.sleep(3)              # folga: bateria/ESC/mecanica se recuperam
    return True


def main(direcao=DIRECAO, nome_csv=NOME_CSV,
         angulo_inicial=ANGULO_INICIAL, angulo_final=ANGULO_FINAL):
    if direcao == "descida":
        escada = range(angulo_final, angulo_inicial - 1, -1)
    else:
        escada = range(angulo_inicial, angulo_final + 1)

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with instancia_unica(LOCK_PATH):
        aquecer_tunel()
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
                        rodar_degrau(ser, csv_writer, angulo, t_ensaio0)
                except KeyboardInterrupt:
                    log.warning("Ensaio interrompido pelo usuario; "
                                "enviando neutro e fechando o CSV.")
                    garantir_neutro()
                    return
    log.info("Ensaio completo. CSV salvo em %s", nome_csv)


if __name__ == "__main__":
    main()
