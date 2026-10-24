"""Ensaio CEGO de descida (120 -> 98): mesmo programa, escada invertida.

Rode DEPOIS da subida (rodar_ensaio_cego.py), com pausa de ~60 s
entre as series para a bateria/ESC se recuperarem."""

from rodar_ensaio_cego import main

if __name__ == "__main__":
    main(direcao="descida", nome_csv="ensaio_cego_descida.csv",
         angulo_inicial=117, angulo_final=98)
