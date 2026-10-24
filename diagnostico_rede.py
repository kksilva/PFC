"""Diagnostico rapido da rede notebook <-> Raspberry Pi.

RODE ESTANDO NA REDE DO PI (iwgetid -r deve mostrar o SSID dele).
Responde: o link aguenta o modo confirmado? e o uso do cabo/Ethernet?

Uso: python3 diagnostico_rede.py
"""

import statistics
import subprocess
import time

PI = "alunos@raspberrypi.local"


def ping():
    r = subprocess.run(["ping", "-c", "10", "-i", "0.3", "-W", "2",
                        "raspberrypi.local"],
                       capture_output=True, text=True)
    for linha in r.stdout.splitlines():
        if "min/avg/max" in linha or "rtt" in linha:
            # min/avg/max/mdev = 1.2/3.4/5.6/0.7 ms
            partes = linha.split("=")[1].split("/")
            return [float(p.replace(" ms", "")) for p in partes[:4]]
    return None


def ssh_latencia(n=5):
    tempos, falhas = [], 0
    for _ in range(n):
        t = time.time()
        try:
            r = subprocess.run(["ssh", "-o", "ConnectTimeout=8",
                                "-o", "BatchMode=yes", PI, "true"],
                               capture_output=True, timeout=15)
            if r.returncode == 0:
                tempos.append(time.time() - t)
            else:
                falhas += 1
        except subprocess.TimeoutExpired:
            falhas += 1
    return tempos, falhas


def main():
    print("== Diagnostico de rede notebook <-> Pi ==")
    p = ping()
    if p is None:
        print("ping: FALHOU - Pi inalcancavel (rede errada? Pi desligado?)")
        return
    print(f"ping: min {p[0]:.1f} ms | medio {p[1]:.1f} ms | max {p[2]:.1f} ms "
          f"| jitter {p[3]:.1f} ms")

    ts, falhas = ssh_latencia()
    if ts:
        print(f"ssh : min {min(ts):.2f} s | medio {statistics.mean(ts):.2f} s "
              f"| max {max(ts):.2f} s | falhas {falhas}/5")
    else:
        print(f"ssh : TODAS as {falhas} tentativas falharam")

    if p[1] < 100 and ts and statistics.mean(ts) < 0.5 and falhas == 0:
        print("\nVEREDITO: link BOM - pode usar o modo confirmado sem medo.")
    elif ts and falhas <= 2:
        print("\nVEREDITO: link RUIM (lento/instavel) - use o modo CEGO; "
              "considere cabo Ethernet entre notebook e Pi.")
    else:
        print("\nVEREDITO: link INUTILIZAVEL - cabo Ethernet ou Pi off-car. "
              "Nenhum timeout de software resolve perda de pacotes.")


if __name__ == "__main__":
    main()
