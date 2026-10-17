#!/usr/bin/env python3
# Teste direto do ESC no canal 1 do PCA9685.
import argparse
import math
import signal
import sys
import time

from adafruit_servokit import ServoKit

CANAL_THROTTLE = 1
ANGULO_NEUTRO = 95.0


def angulo_valido(valor):
    try:
        numero = float(valor)
    except ValueError as exc:
        raise argparse.ArgumentTypeError('Informe um numero.') from exc
    if not math.isfinite(numero):
        raise argparse.ArgumentTypeError('O valor deve ser finito.')
    return numero


def main():
    parser = argparse.ArgumentParser(description='Comanda o throttle por um tempo e retorna ao neutro.')
    parser.add_argument('angulo', type=angulo_valido, help='Angulo do throttle em graus (0 a 180).')
    parser.add_argument('tempo', type=angulo_valido, help='Duracao do comando em segundos (> 0).')
    args = parser.parse_args()
    if not 0 <= args.angulo <= 180:
        parser.error('O angulo deve estar entre 0 e 180 graus.')
    if args.tempo <= 0:
        parser.error('O tempo deve ser maior que zero.')

    kit = ServoKit(channels=16)
    servo = kit.servo[CANAL_THROTTLE]
    interrompido = False

    def interromper(signum, frame):
        nonlocal interrompido
        interrompido = True

    signal.signal(signal.SIGINT, interromper)
    signal.signal(signal.SIGTERM, interromper)

    try:
        servo.angle = ANGULO_NEUTRO
        print(f'ESC em neutro ({ANGULO_NEUTRO:g} graus).', flush=True)
        time.sleep(1.0)
        if not interrompido:
            servo.angle = args.angulo
            print(f'Throttle: {args.angulo:g} graus por {args.tempo:g} s.', flush=True)
            fim = time.monotonic() + args.tempo
            while not interrompido and time.monotonic() < fim:
                time.sleep(min(0.05, max(0, fim - time.monotonic())))
    finally:
        servo.angle = ANGULO_NEUTRO
        print(f'Throttle retornou ao neutro ({ANGULO_NEUTRO:g} graus).', flush=True)


if __name__ == '__main__':
    try:
        main()
    except (OSError, RuntimeError) as exc:
        print(f'Erro ao acessar o controlador de servos: {exc}', file=sys.stderr)
        sys.exit(1)
