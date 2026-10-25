"""Consolidacao e auditoria de TODOS os dados de ensaio (subida/descida/vazio).

Para cada execucao de degrau em cada CSV: separa execucoes, mede pico/plato/
fase de aderencia, detecta falhas (sinal fraco, quedas de linha da serial,
duracao curta) e aplica as regras de validade. Gera:

  - relatorio no terminal (matriz de cobertura por degrau/direcao);
  - ensaio_consolidado.csv : uma linha por execucao valida, com correntes
    prontas para a curva (plato e fase de aderencia).

Regras de validade (carregado, com halteres):
  degrau 99-100 : pico < 1.0 A                     -> invalido (sinal fraco)
  degrau >  100 : pico < 3.0 A                     -> invalido (sinal fraco;
                                                    LVC/bateria/throttle morto)
  duracao < 10 s                                 -> invalido (curto)
  perdas de serial (somatorio de gaps > 1 s)      -> flag PARCIAL
"""

import csv
import os
from collections import defaultdict

ARQUIVOS_CARREGADO = ["ensaio_cego_subida.csv", "ensaio_cego_descida.csv",
                      "ensaio_series_subida.csv", "ensaio_series.csv"]
ARQUIVO_VAZIO = "ensaio_series_vazio.csv"
SAIDA = "ensaio_consolidado.csv"


def carregar(nome):
    rows = []
    if not os.path.exists(nome):
        return rows
    with open(nome) as f:
        rd = csv.reader(f, delimiter=";")
        next(rd, None)
        for r in rd:
            if len(r) == 4:
                try:
                    rows.append((float(r[0]), float(r[1]), int(r[2]),
                                 float(r[3])))
                except ValueError:
                    continue
    return rows


def separar_execs(rows):
    execs, ult_td, ult_a = [], 999.0, None
    for te, td, a, i in rows:
        if a != ult_a or td < ult_td - 1.0:
            execs.append({"ang": a, "te0": te, "L": []})
            ult_a = a
        execs[-1]["L"].append((td, i))
        ult_td = td
    return execs


def media(v):
    return sum(v) / len(v) if v else float("nan")


def avaliar(exec_, taxa_alta):
    L = exec_["L"]
    a = exec_["ang"]
    dur = max((t for t, _ in L), default=0)
    pico = max((i for t, i in L if 1 <= t <= dur - 1), default=0)
    plato = media([i for t, i in L if 5 <= t <= min(12, dur - 1)])
    ader = media([i for _, i in L if i >= 0.6 * pico]) if pico > 0 else 0.0
    deltas = sorted(L[k + 1][0] - L[k][0] for k in range(len(L) - 1))
    nz = [d for d in deltas if d > 0]          # ignora deltas 0 (arred. de 0,1 s)
    dt = nz[len(nz) // 2] if nz else 0.05
    gaps = sum(d - dt for d in deltas if d > 3 * dt)
    motivos = []
    if dur < 10:
        motivos.append("CURTO")
    if pico > 60:
        motivos.append("CORROMPIDO")   # linhas corrompidas da serial (era 115200)
    if pico < 1.0 and a >= 99 or (a > 100 and pico < 3.0):
        motivos.append("SINAL_FRACO")
    if gaps > 3.0:
        motivos.append("PARCIAL")      # so invalida se a perda for severa
    exec_.update(dur=dur, pico=pico, plato=plato, ader=ader,
                 gaps=gaps, motivos=motivos)
    return exec_


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("=" * 72)
    print("AUDITORIA DOS DADOS CARREGADOS (ancorado, com halteres)")
    print("=" * 72)

    cobertura = defaultdict(lambda: {"subida": [], "descida": []})
    linhas_saida = []

    for nome in ARQUIVOS_CARREGADO:
        rows = carregar(nome)
        if not rows:
            continue
        taxa = len(rows) / max(rows[-1][0] - rows[0][0], 1)
        execs = separar_execs(rows)
        print(f"\n## {nome}: {len(rows)} linhas (~{taxa:.0f}/s), "
              f"{len(execs)} execucoes")
        fixo = None
        if "descida" in nome:
            fixo = "descida"
        elif "subida" in nome:
            fixo = "subida"
        sentido = fixo or "subida"
        ult_a = None
        for e in execs:
            if fixo:
                sentido = fixo
            elif ult_a is not None:
                sentido = "subida" if e["ang"] > ult_a else "descida"
            ult_a = e["ang"]
            avaliar(e, taxa > 10)
            ok = not e["motivos"]
            marca = "OK " if ok else "X  "
            print(f"  {marca}{sentido[:3]} {e['ang']:>3} | dur {e['dur']:4.0f}s "
                  f"| pico {e['pico']:5.1f} | plato {e['plato']:5.2f} "
                  f"| ader {e['ader']:5.1f} | gaps {e['gaps']:4.1f}s "
                  f"| {','.join(e['motivos'])}")
            if ok:
                cobertura[e["ang"]][sentido].append(e)
                linhas_saida.append([nome, sentido, e["ang"], e["te0"],
                                     f"{e['pico']:.1f}", f"{e['plato']:.2f}",
                                     f"{e['ader']:.2f}", len(e["L"])])
            else:
                linhas_saida.append([nome, sentido, e["ang"], e["te0"],
                                     f"{e['pico']:.1f}", f"{e['plato']:.2f}",
                                     f"{e['ader']:.2f}", len(e["L"]),
                                     "INVALIDO:" + ",".join(e["motivos"])])

    print("\n" + "=" * 72)
    print("MATRIZ DE COBERTURA (execucoes validas por degrau)")
    print("=" * 72)
    print(f"{'ang':>4} {'subida':>14} {'descida':>14}")
    for a in sorted(cobertura):
        s = cobertura[a]["subida"]
        d = cobertura[a]["descida"]
        fs = f"{len(s)}x | ader {media([e['ader'] for e in s]):5.1f} A" if s else "-"
        fd = f"{len(d)}x | ader {media([e['ader'] for e in d]):5.1f} A" if d else "-"
        print(f"{a:>4} {fs:>14} {fd:>14}")

    n_ok = sum(1 for l in linhas_saida if len(l) == 8)
    print(f"\nExecucoes validas: {n_ok} | invalidas: {len(linhas_saida) - n_ok}")

    with open(SAIDA, "w", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["arquivo", "direcao", "angulo", "t_ensaio_s",
                    "pico_a", "plato_a", "aderencia_a", "n_leituras", "obs"])
        for l in linhas_saida:
            w.writerow(l)
    print(f"Consolidado salvo em {SAIDA}")


if __name__ == "__main__":
    main()
