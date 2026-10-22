import serial
import subprocess
import time

ANGULO_INICIAL = 98
ANGULO_FINAL = 105
DURACAO = 15
NOME_CSV = "ensaio.csv"

PI = "alunos@raspberrypi.local"

ser = serial.Serial("/dev/ttyACM0", 115200, timeout=3)
time.sleep(2)
ser.reset_input_buffer()

t_ensaio = time.time()
csv = open(NOME_CSV, "a")
if csv.tell() == 0:
    csv.write("t_ensaio_s;t_degrau_s;angulo;corrente_a\n")

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
            csv.write(f"{time.time() - t_ensaio:.1f};{time.time() - t0:.1f};"
                      f"{angulo};{corrente}\n")
            csv.flush()
            print(f"  degrau {angulo} | t={time.time() - t0:.1f}s | I={corrente:.2f} A",
                  flush=True)
    proc.wait(timeout=20)   # garante que o Pi terminou (ESC no neutro)
    time.sleep(3)           # folga: bateria/ESC/mecanica se recuperam
    print(f"### fim do degrau {angulo} ###", flush=True)

csv.close()
print("Ensaio completo. CSV salvo em", NOME_CSV)
