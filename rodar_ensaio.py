import serial
import subprocess
import time
import os
import fcntl
import select

ANGULO_INICIAL = 105
ANGULO_FINAL = 115
DURACAO = 15
NOME_CSV = "ensaio_subida_2.csv"

PI = "alunos@raspberrypi.local"

# conexao reutilizada entre degraus (ControlMaster): a 1a abre o tunel,
# as demais sao instantaneas; falha rapida se a rede cair (nao trava)
SSH_CMD = ["ssh",
           "-o", "ControlMaster=auto",
           "-o", "ControlPersist=600",
           "-o", "ControlPath=/tmp/pfc-ssh.sock",
           "-o", "ConnectTimeout=10",
           "-o", "BatchMode=yes",
           PI, "python3 /home/alunos/teste_throttle.py"]

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # CSV sempre na pasta do script

# so uma instancia por vez: se outro rodar_ensaio estiver vivo, aborta
lock = open(".rodar_ensaio.lock", "w")
try:
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
except OSError:
    print("ERRO: outra instancia do script ja esta rodando. Feche-a antes.")
    raise SystemExit(1)

ser = serial.Serial("/dev/ttyACM0", 115200, timeout=3)
time.sleep(2)
ser.reset_input_buffer()

t_ensaio = time.time()
if not os.path.exists(NOME_CSV) or os.path.getsize(NOME_CSV) == 0:
    csv = open(NOME_CSV, "w", buffering=1)   # linha a linha: cada medida vai pro disco na hora
    csv.write("t_ensaio_s;t_degrau_s;angulo;corrente_a\n")
else:
    csv = open(NOME_CSV, "a", buffering=1)   # continua no arquivo existente, nao apaga nada

for angulo in range(ANGULO_INICIAL, ANGULO_FINAL + 1):
    print(f"### DEGRAU {angulo} | enviado {time.strftime('%H:%M:%S')} ###", flush=True)
    proc = subprocess.Popen(SSH_CMD + [str(angulo), str(DURACAO)],
                            stdout=subprocess.PIPE, text=True)

    # sincroniza com o Pi: so comeca a contar o degrau quando ele confirmar o throttle
    t0 = None
    limite = time.time() + 25
    while time.time() < limite and t0 is None:
        prontos, _, _ = select.select([proc.stdout], [], [], 1)
        if not prontos:
            continue
        saida = proc.stdout.readline()
        if not saida:
            break
        print(f"  pi> {saida.strip()}", flush=True)
        if "Throttle:" in saida:
            t0 = time.time()
    if t0 is None:
        proc.kill()
        print("AVISO: Pi nao confirmou o degrau; neutro enviado e degrau pulado", flush=True)
        subprocess.run(SSH_CMD + ["95", "2"])   # garante ESC no neutro
        time.sleep(3)
        continue

    ser.reset_input_buffer()   # descarta linhas velhas: so le o que for deste degrau
    fim = t0 + DURACAO
    while time.time() < fim:
        linha = ser.readline().decode(errors="replace")
        if "Corrente:" in linha:
            corrente = float(linha.split("Corrente:")[1].split()[0])
        elif "ADC:" in linha:
            corrente = (float(linha.split("ADC:")[1].split()[0]) * 3.3 / 4095
                        - 1.65) / 0.0066
        else:
            continue
        csv.write(f"{time.time() - t_ensaio:.1f};{time.time() - t0:.1f};"
                  f"{angulo};{corrente:.2f}\n")
        csv.flush()
        print(f"  t={time.time() - t0:.1f}s | I={corrente:.2f} A", flush=True)

    try:
        proc.wait(timeout=30)   # garante que o Pi voltou ao neutro
    except subprocess.TimeoutExpired:
        proc.kill()
        print("AVISO: Pi nao confirmou o neutro; reenviando", flush=True)
        subprocess.run(SSH_CMD + ["95", "2"])
    time.sleep(3)           # folga: bateria/ESC/mecanica se recuperam
    print(f"### fim do degrau {angulo} ###", flush=True)

csv.close()
print("Ensaio completo. CSV salvo em", NOME_CSV)
