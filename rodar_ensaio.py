import serial
import subprocess
import time
import os

ANGULO_INICIAL = 98
ANGULO_FINAL = 105
DURACAO = 15
NOME_CSV = "ensaio_subida.csv"

PI = "alunos@raspberrypi.local"

ser = serial.Serial("/dev/ttyACM0", 115200, timeout=3)
time.sleep(2)
ser.reset_input_buffer()

SERIE = 1
vazio = not os.path.exists(NOME_CSV) or os.path.getsize(NOME_CSV) == 0
if not vazio:
    with open(NOME_CSV) as f:
        SERIE = sum(1 for linha in f if linha.startswith("#")) + 1

t_ensaio = time.time()
csv = open(NOME_CSV, "a")
csv.write(f"# SERIE {SERIE} | inicio {time.strftime('%d/%m/%Y %H:%M:%S')}\n")
if vazio:
    csv.write("serie;t_ensaio_s;t_degrau_s;angulo;corrente_a\n")

for angulo in range(ANGULO_INICIAL, ANGULO_FINAL + 1):
    t0 = time.time()
    print(f"### DEGRAU {angulo} | inicio {time.strftime('%H:%M:%S')}"
          f" | fim {time.strftime('%H:%M:%S', time.localtime(t0 + DURACAO))} ###",
          flush=True)
    proc = subprocess.Popen(["ssh", PI, "python3 /home/alunos/teste_throttle.py",
                             str(angulo), str(DURACAO)])
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
        csv.write(f"{SERIE};{time.time() - t_ensaio:.1f};{time.time() - t0:.1f};"
                  f"{angulo};{corrente:.2f}\n")
        csv.flush()
        print(f"  degrau {angulo} | t={time.time() - t0:.1f}s | I={corrente:.2f} A",
              flush=True)
    try:
        proc.wait(timeout=60)   # garante que o Pi terminou (ESC no neutro)
    except subprocess.TimeoutExpired:
        print("AVISO: Pi demorou > 60 s, seguindo mesmo assim", flush=True)
    time.sleep(3)           # folga: bateria/ESC/mecanica se recuperam
    print(f"### fim do degrau {angulo} ###", flush=True)

csv.close()
print("Ensaio completo. CSV salvo em", NOME_CSV)
