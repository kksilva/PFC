"""Ensaio de caracterizacao torque x corrente do automodelo.

Aplica degraus de throttle via Raspberry Pi (teste_throttle.py), le a
corrente do ACS758 na serial do Arduino Due e grava um CSV linha a
linha. A janela de 15 s de cada degrau so comeca quando o Pi confirma
o comando. O Pi e invocado com `python3 -u` (sem buffer de saida), para
que a confirmacao chegue no instante real do throttle. Ao lado de cada
leitura, imprime a media movel; ao fim de cada degrau, detecta
patinagem (queda brusca de corrente) e reporta a media pre-patinagem.
"""

import csv
import fcntl
import logging
import os
import select
import subprocess
import sys
import time
from collections import deque
from contextlib import contextmanager
from serial import Serial

# ---------------------------------------------------------------- config do ensaio
ANGULO_INICIAL = 105          # primeiro degrau da escada
ANGULO_FINAL = 115            # ultimo degrau da escada
DURACAO_S = 15                # duracao de cada degrau
DIRECAO = "subida"            # "subida": INICIAL->FINAL | "descida": FINAL->INICIAL
NOME_CSV = "ensaio_teste.csv"
RETENTATIVAS = 3              # tentativas de confirmacao do Pi antes de pular o degrau
INICIO_JANELA_S = 7           # t_degrau a partir do qual o regime e valido (media final)
JANELA_MM = 10                # leituras da media movel exibida ao lado de cada I
PRINT_A_CADA = 10             # no terminal, imprime 1 a cada N leituras
                              # (CSV sempre grava tudo; 10 => 100 Hz vira 1 print/s)
LIMIAR_PATINAGEM = 0.3        # corrente < 30% do pico apos t>=2 s => patinagem
ESPERA_PI_S = 90              # tempo maximo aguardando o Pi voltar (ex.: apos reboot)

# ---------------------------------------------------------------- hardware
PORTA_SERIAL = "/dev/ttyACM0"
BAUD = 115200
PI = "alunos@raspberrypi.local"
COMANDO_PI = "python3 -u /home/alunos/teste_throttle.py"   # -u: sem buffer de saida
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
SOQUETE_SSH = "/tmp/pfc-ssh.sock"
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
def tunel_ok():
    """True se o soquete mestre do ssh ainda estiver vivo."""
    r = subprocess.run(["ssh", "-O", "check"] + SSH_TUNNEL_OPTS + [PI],
                       capture_output=True, timeout=10)
    return r.returncode == 0


def medir_latencia():
    """Tempo de uma execucao trivial no Pi; None se inalcancavel."""
    t = time.time()
    try:
        r = subprocess.run(["ssh"] + SSH_TUNNEL_OPTS + [PI, "true"],
                           capture_output=True, timeout=15)
    except subprocess.TimeoutExpired:
        return None
    return time.time() - t if r.returncode == 0 else None


def garantir_tunel():
    """Aguarda o Pi ficar alcancavel, recriando o tunel se preciso.

    Em degraus altos o Pi pode sofrer brown-out e reiniciar (boot ~40-60 s);
    em vez de desistir rapido, espera ate ESPERA_PI_S."""
    limite = time.time() + ESPERA_PI_S
    while time.time() < limite:
        lat = medir_latencia()
        if lat is not None:
            if lat > 3:
                log.warning("rede lenta (latencia %.1f s); link pode cair neste degrau", lat)
            return
        restam = int(limite - time.time())
        log.warning("Pi inalcancavel; recriando tunel e aguardando (%d s restantes)...",
                    restam)
        subprocess.run(["rm", "-f", SOQUETE_SSH])
        subprocess.run(["ssh", "-Nf"] + SSH_TUNNEL_OPTS + [PI], timeout=20)
        time.sleep(5)
    log.error("Pi NAO voltou em %d s; degrau sera pulado. "
              "Verifique alimentacao/cabo do Pi.", ESPERA_PI_S)


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


def aguardar_confirmacao(proc, angulo):
    """Espera o Pi confirmar 'Throttle: <angulo>'; retorna o t0 real ou None."""
    limite = time.time() + TIMEOUT_CONFIRMACAO_S
    while time.time() < limite:
        prontos, _, _ = select.select([proc.stdout], [], [], 1)
        if not prontos:
            continue
        saida = proc.stdout.readline()
        if not saida:
            return None
        log.info("pi> %s", saida.strip())
        if "Throttle:" in saida and str(angulo) in saida:
            return time.time()
    return None


def limpar_pi():
    """Mata processos remotos de throttle que tenham ficado orfaos no Pi."""
    subprocess.run(["ssh"] + SSH_TUNNEL_OPTS + [PI, "pkill", "-f",
                                                "teste_throttle.py"],
                   capture_output=True, timeout=15)


def garantir_neutro():
    """Forca o ESC de volta ao neutro (seguranca do veiculo)."""
    garantir_tunel()
    limpar_pi()
    subprocess.run(["ssh"] + SSH_TUNNEL_OPTS + [PI, COMANDO_PI,
                                                str(NEUTRO_GRAUS), "2"])


# ---------------------------------------------------------------- nucleo do ensaio
def resumo_degrau(angulo, leituras):
    """Reporta a media da janela, a fase de aderencia e a patinagem.

    Patinagem = queda SUSTENTADA no meio da janela (o fim do degrau, em
    que o throttle termina e I->0, nao conta). Em regime de patinagem
    ciclica (aderencia alternando com deslizamento), a media da janela e
    sem sentido: usa-se a fase de aderencia (pontos >= 60% do pico)."""
    dur = max((t for t, _ in leituras), default=DURACAO_S)
    pico = max((i for t, i in leituras if 1 <= t <= dur - 1), default=float("nan"))
    t_patinagem = None
    for k, (t, i) in enumerate(leituras):
        if t < 2 or t > dur - 2:
            continue
        if i < LIMIAR_PATINAGEM * pico:
            seguintes = [j for _, j in leituras[k:k + 4]]
            if media(seguintes) < 0.4 * pico:
                t_patinagem = t
                break
    aderencia = [i for _, i in leituras if i >= 0.6 * pico]
    if t_patinagem is not None:
        validas = [i for t, i in leituras if t < t_patinagem]
        log.info(">> DEGRAU %d: PATINAGEM sustentada em t=%.1fs | media pre-patinagem "
                 "= %.2f A | fase de aderencia = %.2f A (n=%d)", angulo, t_patinagem,
                 media(validas), media(aderencia), len(aderencia))
    else:
        log.info(">> DEGRAU %d: media janela = %.2f A | fase de aderencia = %.2f A "
                 "(n=%d, pico %.1f A)", angulo, media([i for _, i in leituras]),
                 media(aderencia), len(aderencia), pico)


def rodar_degrau(ser, csv_writer, angulo, t_ensaio0):
    """Aplica um degrau, sincroniza com o Pi, le a serial e grava.
    Retorna True se o degrau foi executado e confirmado."""
    log.info("### DEGRAU %d ###", angulo)

    t0 = None
    for tentativa in range(1, RETENTATIVAS + 1):
        garantir_tunel()
        limpar_pi()                # garante que nenhum throttle orfao segue no Pi
        proc = enviar_comando(angulo, DURACAO_S)
        t0 = aguardar_confirmacao(proc, angulo)
        if t0 is not None:
            break
        proc.kill()
        limpar_pi()                # se conectou e rodou, mata antes de reenviar
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
    mm = deque(maxlen=JANELA_MM)
    n_leitura = 0
    fim = t0 + DURACAO_S
    while time.time() < fim:
        corrente = extrair_corrente(ser.readline().decode(errors="replace"))
        if corrente is None:
            continue
        mm.append(corrente)
        n_leitura += 1
        t_degrau = time.time() - t0
        csv_writer.writerow([f"{time.time() - t_ensaio0:.1f}", f"{t_degrau:.1f}",
                             angulo, f"{corrente:.2f}"])
        leituras.append((t_degrau, corrente))
        if n_leitura % PRINT_A_CADA == 0:
            print(f"  t={t_degrau:.1f}s | I={corrente:.2f} A | MM={media(mm):.2f} A",
                  flush=True)

    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill()
        log.warning("Pi nao confirmou o neutro; reenviando")
        garantir_neutro()

    resumo_degrau(angulo, leituras)
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
                    return False
    log.info("Ensaio completo. CSV salvo em %s", nome_csv)
    return True


if __name__ == "__main__":
    main()
