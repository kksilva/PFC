import serial
import subprocess
import time
import os
import fcntl

ANGULO_INICIAL = 115
ANGULO_FINAL = 95
DURACAO = 15
NOME_CSV = "ensaio_descida.csv"

PI = "alunos@raspberrypi.local"

# conexao reutilizada entre degraus (ControlMaster): a 1a abre o tunel,
# as demais sao instantaneas; falha rapida se a rede cair (nao trava 60 s)
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

for angulo in range(ANGULO_INICIAL, ANGULO_FINAL - 1, -1):
    t0 = time.time()
    ser.reset_input_buffer()   # descarta linhas velhas: so le o que for deste degrau
    print(f"### DEGRAU {angulo} | inicio {time.strftime('%H:%M:%S')}"
          f" | fim {time.strftime('%H:%M:%S', time.localtime(t0 + DURACAO))} ###",
          flush=True)
    proc = subprocess.Popen(SSH_CMD + [str(angulo), str(DURACAO)])
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
        proc.wait(timeout=DURACAO + 30)   # garante que o Pi terminou (ESC no neutro)
    except subprocess.TimeoutExpired:
        proc.kill()
        print("AVISO: Pi nao respondeu; comando de neutro reenviado", flush=True)
        subprocess.run(SSH_CMD + ["95", "2"])   # forca neutro antes do proximo degrau
    time.sleep(3)           # folga: bateria/ESC/mecanica se recuperam
    print(f"### fim do degrau {angulo} ###", flush=True)

csv.close()
print("Ensaio completo. CSV salvo em", NOME_CSV)
