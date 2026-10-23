#!/bin/bash
# Compila a monografia e abre o PDF atualizado.
# Uso: ./compilar.sh
set -e
cd "$(dirname "$0")"
latexmk -pdf -interaction=nonstopmode Monografia.tex
xdg-open Monografia.pdf >/dev/null 2>&1 &
